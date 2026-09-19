import unittest

from models.result import Result
from models.student import Student
from utils.exceptions import ValidationError

STUDENT_ARGS = ("SE00001", "Nguyen Van An", "15/03/2005", "Male", "SE1901",
                "0901234567", "an.nguyen@fpt.edu.vn", "Active")


class StudentTests(unittest.TestCase):
    def test_create_and_str(self):
        student = Student(*STUDENT_ARGS)
        self.assertIn("SE00001", str(student))
        self.assertTrue(student.is_active)

    def test_student_id_is_read_only(self):
        student = Student(*STUDENT_ARGS)
        with self.assertRaises(AttributeError):
            student.student_id = "SE99999"

    def test_setter_validates(self):
        student = Student(*STUDENT_ARGS)
        with self.assertRaises(ValidationError):
            student.phone = "abc"
        student.phone = "0912345678"
        self.assertEqual(student.phone, "0912345678")

    def test_update_rejects_unknown_field(self):
        with self.assertRaises(ValidationError):
            Student(*STUDENT_ARGS).update(student_id="SE00002")

    def test_record_round_trip(self):
        student = Student(*STUDENT_ARGS)
        again = Student.from_record(student.to_record())
        self.assertEqual(again.to_dict(), student.to_dict())
        with self.assertRaises(ValidationError):
            Student.from_record(["only", "three", "fields"])


class ResultTests(unittest.TestCase):
    def make(self, fe=None, re=None):
        return Result("SE00001", "PFP191", "Programming Fundamentals with Python",
                      "Fall2026", 3, fe, re)

    def test_pass_rule(self):
        cases = [(7.0, None, "Pass"), (5.0, None, "Pass"), (4.9, 5.0, "Pass"),
                 (4.0, 4.0, "Fail"), (4.0, None, "Fail"), (None, None, "Pending")]
        for fe, re, expected in cases:
            with self.subTest(fe=fe, re=re):
                self.assertEqual(self.make(fe, re).status, expected)

    def test_max_two_attempts_rules(self):
        with self.assertRaises(ValidationError):
            self.make(None, 6.0)          # RE khi chưa có FE
        with self.assertRaises(ValidationError):
            self.make(6.0, 7.0)           # RE khi FE đã đạt

    def test_grade_setter_recalculates_status(self):
        result = self.make(3.0)
        self.assertEqual(result.status, "Fail")
        result.grade_re = 6.0
        self.assertEqual(result.status, "Pass")
        self.assertEqual(result.final_grade, 6.0)

    def test_record_round_trip_keeps_blank_grades(self):
        result = self.make(3.0)
        record = result.to_record()
        self.assertEqual(record[6], "")   # RE để trống
        again = Result.from_record(record)
        self.assertIsNone(again.grade_re)
        self.assertEqual(again.status, "Fail")


if __name__ == "__main__":
    unittest.main()
