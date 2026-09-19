import unittest

from utils import validators as v
from utils.exceptions import ValidationError


class ValidatorTests(unittest.TestCase):
    def test_student_id(self):
        self.assertEqual(v.validate_student_id(" se00001 "), "SE00001")
        for bad in ("", "S001", "SE0001", "SE000001", "1234567"):
            with self.assertRaises(ValidationError):
                v.validate_student_id(bad)

    def test_full_name(self):
        self.assertEqual(v.validate_full_name("  nguyen   van an "), "Nguyen Van An")
        for bad in ("An", "Nguyen Van 3", "Nguyen|Van"):
            with self.assertRaises(ValidationError):
                v.validate_full_name(bad)

    def test_date_of_birth(self):
        self.assertEqual(v.validate_date_of_birth("5/3/2005"), "05/03/2005")
        for bad in ("31/02/2005", "2005-03-15", "15/03/2999", "15/03/1900"):
            with self.assertRaises(ValidationError):
                v.validate_date_of_birth(bad)

    def test_gender_phone_email_class(self):
        self.assertEqual(v.validate_gender("f"), "Female")
        self.assertEqual(v.validate_gender("MALE"), "Male")
        self.assertEqual(v.validate_phone("090 123 4567"), "0901234567")
        self.assertEqual(v.validate_email("An.Nguyen@FPT.edu.vn"), "an.nguyen@fpt.edu.vn")
        self.assertEqual(v.validate_class_name("se1901"), "SE1901")
        for func, bad in ((v.validate_gender, "x"), (v.validate_phone, "12345"),
                          (v.validate_email, "a@b"), (v.validate_class_name, "S19")):
            with self.assertRaises(ValidationError):
                func(bad)

    def test_result_fields(self):
        self.assertEqual(v.validate_course_id("pfp191"), "PFP191")
        self.assertEqual(v.validate_semester("fall 2026"), "Fall2026")
        self.assertEqual(v.validate_credits("3"), 3)
        self.assertIsNone(v.validate_grade(""))
        self.assertIsNone(v.validate_grade(None))
        self.assertEqual(v.validate_grade("7,55"), 7.5)  # dấu phẩy + làm tròn 1 chữ số
        for func, bad in ((v.validate_grade, "11"), (v.validate_grade, "-1"),
                          (v.validate_grade, "abc"), (v.validate_credits, "0"),
                          (v.validate_semester, "Autumn2026")):
            with self.assertRaises(ValidationError):
                func(bad)


if __name__ == "__main__":
    unittest.main()
