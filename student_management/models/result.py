"""Model Result: kết quả học tập của một sinh viên trong một môn."""
from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from utils import validators as v
from utils.constants import PASS_SCORE, RESULT_FAIL, RESULT_PASS, RESULT_PENDING
from utils.exceptions import ValidationError

from .base_model import BaseModel


def _format_grade(grade: Optional[float]) -> str:
    return "" if grade is None else f"{grade:.1f}"


class Result(BaseModel):
    FIELDS = (
        "student_id", "course_id", "course_name", "semester",
        "credits", "grade_fe", "grade_re", "status",
    )

    def __init__(
        self,
        student_id: str,
        course_id: str,
        course_name: str,
        semester: str,
        credits: object,
        grade_fe: object = None,
        grade_re: object = None,
        status: Optional[str] = None,
    ) -> None:
        self._student_id = v.validate_student_id(student_id)
        self._course_id = v.validate_course_id(course_id)
        self.course_name = course_name
        self.semester = semester
        self.credits = credits
        self._grade_fe: Optional[float] = None
        self._grade_re: Optional[float] = None
        self._status = RESULT_PENDING
        self.set_grades(grade_fe, grade_re)      # tự tính status
        if status not in (None, ""):             # status lưu trong file (nếu có)
            self.status = status                 # được ưu tiên hơn giá trị tự tính

    # ---- thuộc tính chỉ đọc -------------------------------------------------
    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def course_id(self) -> str:
        return self._course_id

    @property
    def key(self) -> Tuple[str, str]:
        """Khoá nhận diện một kết quả: (student_id, course_id)."""
        return (self._student_id, self._course_id)

    # ---- thuộc tính đọc / ghi -----------------------------------------------
    @property
    def course_name(self) -> str:
        return self._course_name

    @course_name.setter
    def course_name(self, value: str) -> None:
        self._course_name = v.validate_course_name(value)

    @property
    def semester(self) -> str:
        return self._semester

    @semester.setter
    def semester(self, value: str) -> None:
        self._semester = v.validate_semester(value)

    @property
    def credits(self) -> int:
        return self._credits

    @credits.setter
    def credits(self, value: object) -> None:
        self._credits = v.validate_credits(value)

    @property
    def grade_fe(self) -> Optional[float]:
        return self._grade_fe

    @grade_fe.setter
    def grade_fe(self, value: object) -> None:
        self.set_grades(value, self._grade_re)

    @property
    def grade_re(self) -> Optional[float]:
        return self._grade_re

    @grade_re.setter
    def grade_re(self, value: object) -> None:
        self.set_grades(self._grade_fe, value)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = v.validate_result_status(value)

    # ---- thuộc tính suy ra --------------------------------------------------
    @property
    def is_passed(self) -> bool:
        return self._status == RESULT_PASS

    @property
    def final_grade(self) -> Optional[float]:
        """Điểm cuối cùng: điểm RE nếu phải thi lại, ngược lại là điểm FE."""
        if self._grade_fe is None:
            return None
        if self._grade_fe < PASS_SCORE and self._grade_re is not None:
            return self._grade_re
        return self._grade_fe

    # ---- nghiệp vụ ----------------------------------------------------------
    @staticmethod
    def calculate_status(grade_fe: Optional[float], grade_re: Optional[float]) -> str:
        """Pass khi FE >= 5, hoặc (FE < 5 và RE >= 5).

        Chưa có điểm FE -> Pending (chưa chấm). FE < 5 và chưa thi lại -> Fail.
        """
        if grade_fe is None:
            return RESULT_PENDING
        if grade_fe >= PASS_SCORE or (grade_re is not None and grade_re >= PASS_SCORE):
            return RESULT_PASS
        return RESULT_FAIL

    def set_grades(self, grade_fe: object, grade_re: object) -> None:
        """Gán cả hai điểm cùng lúc (validate trọn vẹn trước khi thay đổi) rồi tính lại status.

        Mỗi môn tối đa 2 lần thi: FE và RE. RE chỉ hợp lệ khi đã có FE và FE < 5.
        """
        fe = v.validate_grade(grade_fe, "Grade FE")
        re = v.validate_grade(grade_re, "Grade RE")
        if re is not None:
            if fe is None:
                raise ValidationError("Grade RE cannot be entered before grade FE.")
            if fe >= PASS_SCORE:
                raise ValidationError(
                    "Grade RE is only allowed when FE < 5 (max 2 exam attempts per course)."
                )
        self._grade_fe, self._grade_re = fe, re
        self._status = self.calculate_status(fe, re)

    # ---- chuyển đổi file ----------------------------------------------------
    def to_record(self) -> List[str]:
        return [
            self._student_id, self._course_id, self._course_name, self._semester,
            str(self._credits), _format_grade(self._grade_fe),
            _format_grade(self._grade_re), self._status,
        ]

    @classmethod
    def from_record(cls, values: Sequence[str]) -> "Result":
        if len(values) != len(cls.FIELDS):
            raise ValidationError(
                f"Expected {len(cls.FIELDS)} fields but found {len(values)}."
            )
        return cls(*values)

    # ---- hiển thị -----------------------------------------------------------
    def __str__(self) -> str:
        fe = _format_grade(self._grade_fe) or "-"
        re = _format_grade(self._grade_re) or "-"
        return (
            f"[{self._student_id}] {self._course_id} - {self._course_name} | "
            f"{self._semester} | {self._credits} credits | FE: {fe} | RE: {re} | "
            f"{self._status}"
        )

    def __repr__(self) -> str:
        return f"Result(student_id={self._student_id!r}, course_id={self._course_id!r})"
