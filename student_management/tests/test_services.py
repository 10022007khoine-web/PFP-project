import tempfile
import unittest
from pathlib import Path

from models.result import Result
from models.student import Student
from services import ResultManager, StudentManager
from utils.exceptions import (DuplicateError, FileDataError, NotFoundError,
                              ValidationError)


def make_student(sid="SE00001", cls="SE1901", status="Active"):
    return Student(sid, "Nguyen Van An", "15/03/2005", "Male", cls,
                   "0901234567", "an@fpt.edu.vn", status)


def make_result(sid="SE00001", cid="PFP191", fe=None, re=None):
    return Result(sid, cid, "Some Course", "Fall2026", 3, fe, re)


class StudentManagerTests(unittest.TestCase):
    def setUp(self):
        self.sm = StudentManager()

    def test_add_and_duplicate(self):
        self.sm.add_student(make_student())
        with self.assertRaises(DuplicateError):
            self.sm.add_student(make_student())

    def test_update_is_atomic(self):
        self.sm.add_student(make_student())
        with self.assertRaises(ValidationError):
            self.sm.update_student("SE00001", full_name="Le Van Binh", phone="bad")
        self.assertEqual(self.sm.get_student("SE00001").full_name, "Nguyen Van An")
        self.sm.update_student("se00001", full_name="Le Van Binh", class_name="IT1902")
        self.assertEqual(self.sm.get_student("SE00001").class_name, "IT1902")

    def test_update_missing_student(self):
        with self.assertRaises(NotFoundError):
            self.sm.update_student("SE00099", phone="0901234567")

    def test_filters_and_next_id(self):
        self.sm.add_student(make_student("SE00001", "SE1901", "Active"))
        self.sm.add_student(make_student("SE00002", "IT1902", "Inactive"))
        self.sm.add_student(make_student("SE00003", "SE1901", "Graduated"))
        self.assertEqual([s.student_id for s in self.sm.filter_by_class("se1901")],
                         ["SE00001", "SE00003"])
        self.assertEqual([s.student_id for s in self.sm.filter_by_status("inactive")],
                         ["SE00002"])
        self.assertEqual([s.student_id for s in self.sm.get_active_students()], ["SE00001"])
        self.assertEqual(self.sm.next_student_id(), "SE00004")


class ResultManagerTests(unittest.TestCase):
    def setUp(self):
        self.sm = StudentManager()
        for sid in ("SE00001", "SE00002", "SE00003"):
            self.sm.add_student(make_student(sid))
        self.rm = ResultManager(self.sm)

    def test_add_requires_student_and_unique_key(self):
        with self.assertRaises(NotFoundError):
            self.rm.add_result(make_result("SE00099"))
        self.rm.add_result(make_result())
        with self.assertRaises(DuplicateError):
            self.rm.add_result(make_result())

    def test_update_grade_recalculates_status(self):
        self.rm.add_result(make_result(fe=3.0))
        self.assertEqual(self.rm.get_result("SE00001", "PFP191").status, "Fail")
        self.rm.update_result("SE00001", "PFP191", grade_re=6.0)
        self.assertEqual(self.rm.get_result("SE00001", "PFP191").status, "Pass")

    def test_update_status_manually_and_invalid_update(self):
        self.rm.add_result(make_result(fe=8.0))
        self.rm.update_result("SE00001", "PFP191", status="Fail")
        self.assertEqual(self.rm.get_result("SE00001", "PFP191").status, "Fail")
        with self.assertRaises(ValidationError):
            self.rm.update_result("SE00001", "PFP191", grade_re=9.0)  # FE >= 5
        with self.assertRaises(NotFoundError):
            self.rm.update_result("SE00001", "MAD101", grade_fe=5.0)

    def test_sorted_by_status_descending(self):
        self.rm.add_result(make_result("SE00001", "PFP191", fe=3.0))   # Fail
        self.rm.add_result(make_result("SE00002", "PFP191"))            # Pending
        self.rm.add_result(make_result("SE00003", "PFP191", fe=9.0))   # Pass
        statuses = [r.status for r in self.rm.sorted_by_status()]
        self.assertEqual(statuses, ["Pass", "Fail", "Pending"])
        self.assertEqual([r.student_id for r in self.rm.get_passed_results()], ["SE00003"])

    def test_search_and_summary(self):
        self.rm.add_result(make_result("SE00001", "PFP191", fe=8.0))
        self.rm.add_result(make_result("SE00001", "MAD101", fe=2.0, re=4.0))
        self.assertEqual(len(self.rm.find_by_student("se00001")), 2)
        summary = self.rm.summary("SE00001")
        self.assertEqual((summary["courses"], summary["passed"]), (2, 1))
        self.assertEqual(summary["passed_credits"], 3)
        self.assertAlmostEqual(summary["average"], 6.0)   # (8*3 + 4*3) / 6


class FileTests(unittest.TestCase):
    def test_round_trip(self):
        sm = StudentManager()
        sm.add_student(make_student())
        rm = ResultManager(sm)
        rm.add_result(make_result(fe=3.0, re=6.0))
        with tempfile.TemporaryDirectory() as folder:
            s_path, r_path = Path(folder, "s.txt"), Path(folder, "r.txt")
            sm.save_to_file(s_path)
            rm.save_to_file(r_path)

            sm2 = StudentManager(); rm2 = ResultManager(sm2)
            self.assertEqual(sm2.load_from_file(s_path), (1, []))
            self.assertEqual(rm2.load_from_file(r_path), (1, []))
            self.assertEqual(rm2.get_result("SE00001", "PFP191").status, "Pass")

    def test_bad_lines_are_reported_not_fatal(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder, "s.txt")
            path.write_text(
                "# header\n"
                "SE00001|Nguyen Van An|15/03/2005|Male|SE1901|0901234567|an@fpt.edu.vn|Active\n"
                "SE00001|Trung Ma|15/03/2005|Male|SE1901|0901234567|x@fpt.edu.vn|Active\n"
                "SE00002|Thieu Truong|15/03/2005\n"
                "SE00003|Sai Dien Thoai|15/03/2005|Male|SE1901|123|x@fpt.edu.vn|Active\n"
                "\n",
                encoding="utf-8")
            sm = StudentManager()
            count, errors = sm.load_from_file(path)
            self.assertEqual(count, 1)
            self.assertEqual(len(errors), 3)

    def test_missing_file_raises(self):
        with self.assertRaises(FileDataError):
            StudentManager().load_from_file("does/not/exist.txt")


if __name__ == "__main__":
    unittest.main()
