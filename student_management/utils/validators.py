"""Các hàm kiểm tra (validate) và chuẩn hoá dữ liệu.

Mỗi hàm nhận giá trị thô, trả về giá trị đã chuẩn hoá, hoặc ném ValidationError.
"""
from __future__ import annotations

import re
from datetime import date, datetime
from typing import Optional, Sequence

from .constants import (
    DELIMITER,
    GENDERS,
    MAX_AGE,
    MAX_CREDITS,
    MAX_GRADE,
    MIN_AGE,
    MIN_CREDITS,
    RESULT_STATUSES,
    STUDENT_STATUSES,
)
from .exceptions import ValidationError

_STUDENT_ID_RE = re.compile(r"^[A-Z]{2}\d{5}$")                 # SE00001
_CLASS_RE = re.compile(r"^[A-Z]{2,3}\d{4}$")                    # SE1901, IT1902
_PHONE_RE = re.compile(r"^0\d{9}$")                             # 0901234567
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
_COURSE_ID_RE = re.compile(r"^[A-Z]{3}\d{3}$")                  # PFP191
_SEMESTER_RE = re.compile(r"^(spring|summer|fall)(\d{4})$", re.IGNORECASE)
_GENDER_ALIASES = {"m": "Male", "f": "Female"}
DATE_FORMAT = "%d/%m/%Y"


def _clean_text(value: object, field: str) -> str:
    """Gộp khoảng trắng thừa, không cho rỗng và không chứa ký tự phân cách file."""
    text = " ".join(str(value).split()) if value is not None else ""
    if not text:
        raise ValidationError(f"{field} must not be empty.")
    if DELIMITER in text:
        raise ValidationError(f"{field} must not contain the character '{DELIMITER}'.")
    return text


def _match_choice(value: object, choices: Sequence[str], field: str) -> str:
    text = _clean_text(value, field)
    for choice in choices:
        if choice.lower() == text.lower():
            return choice
    raise ValidationError(f"{field} must be one of: {', '.join(choices)}.")


# ---------------------------------------------------------------- Student ----
def validate_student_id(value: object) -> str:
    text = _clean_text(value, "Student ID").upper()
    if not _STUDENT_ID_RE.match(text):
        raise ValidationError("Student ID must be 2 letters + 5 digits (e.g. SE00001).")
    return text


def validate_full_name(value: object) -> str:
    text = _clean_text(value, "Full name")
    if not all(ch.isalpha() or ch in " '-" for ch in text):
        raise ValidationError("Full name may only contain letters and spaces.")
    if len(text.split()) < 2:
        raise ValidationError("Full name must contain at least two words.")
    if len(text) > 50:
        raise ValidationError("Full name must not exceed 50 characters.")
    return text.title()


def validate_date_of_birth(value: object) -> str:
    text = _clean_text(value, "Date of birth")
    try:
        dob = datetime.strptime(text, DATE_FORMAT).date()
    except ValueError:
        raise ValidationError("Date of birth must be a valid date in dd/mm/yyyy format.") from None
    today = date.today()
    if dob > today:
        raise ValidationError("Date of birth cannot be in the future.")
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if not MIN_AGE <= age <= MAX_AGE:
        raise ValidationError(f"Student age must be between {MIN_AGE} and {MAX_AGE}.")
    return dob.strftime(DATE_FORMAT)


def validate_gender(value: object) -> str:
    text = _clean_text(value, "Gender")
    return _GENDER_ALIASES.get(text.lower()) or _match_choice(text, GENDERS, "Gender")


def validate_class_name(value: object) -> str:
    text = _clean_text(value, "Class name").upper()
    if not _CLASS_RE.match(text):
        raise ValidationError("Class name must look like SE1901, IT1902 or AI1903.")
    return text


def validate_phone(value: object) -> str:
    text = _clean_text(value, "Phone").replace(" ", "")
    if not _PHONE_RE.match(text):
        raise ValidationError("Phone must have 10 digits and start with 0 (e.g. 0901234567).")
    return text


def validate_email(value: object) -> str:
    text = _clean_text(value, "Email").lower()
    if not _EMAIL_RE.match(text):
        raise ValidationError("Email is not valid (e.g. an.nguyen@fpt.edu.vn).")
    return text


def validate_student_status(value: object) -> str:
    return _match_choice(value, STUDENT_STATUSES, "Status")


# ----------------------------------------------------------------- Result ----
def validate_course_id(value: object) -> str:
    text = _clean_text(value, "Course ID").upper()
    if not _COURSE_ID_RE.match(text):
        raise ValidationError("Course ID must be 3 letters + 3 digits (e.g. PFP191).")
    return text


def validate_course_name(value: object) -> str:
    text = _clean_text(value, "Course name")
    if len(text) > 100:
        raise ValidationError("Course name must not exceed 100 characters.")
    return text


def validate_semester(value: object) -> str:
    text = _clean_text(value, "Semester").replace(" ", "")
    match = _SEMESTER_RE.match(text)
    if not match:
        raise ValidationError("Semester must look like Spring2026, Summer2026 or Fall2026.")
    return f"{match.group(1).capitalize()}{match.group(2)}"


def validate_credits(value: object) -> int:
    try:
        credits = int(str(value).strip())
    except ValueError:
        raise ValidationError("Credits must be an integer.") from None
    if not MIN_CREDITS <= credits <= MAX_CREDITS:
        raise ValidationError(f"Credits must be between {MIN_CREDITS} and {MAX_CREDITS}.")
    return credits


def validate_grade(value: object, field: str = "Grade") -> Optional[float]:
    """Điểm 0-10 (làm tròn 1 chữ số thập phân). Rỗng/None nghĩa là chưa có điểm."""
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip().replace(",", ".")
        if not value:
            return None
    try:
        grade = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        raise ValidationError(f"{field} must be a number between 0 and {MAX_GRADE:g}.") from None
    if not 0 <= grade <= MAX_GRADE:
        raise ValidationError(f"{field} must be between 0 and {MAX_GRADE:g}.")
    return round(grade, 1)


def validate_result_status(value: object) -> str:
    return _match_choice(value, RESULT_STATUSES, "Result status")
