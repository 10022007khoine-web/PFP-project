"""ResultManager: quản lý danh sách kết quả học tập (lưu bằng list[Result])."""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

from models.result import Result
from services.student_manager import StudentManager
from utils import validators as v
from utils.constants import RESULT_FAIL, RESULT_PASS, RESULT_PENDING
from utils.exceptions import (
    DuplicateError,
    NotFoundError,
    StudentManagementError,
    ValidationError,
)
from utils.file_handler import PathLike, read_records, write_records

# Thứ hạng để sắp xếp "giảm dần theo status": Pass -> Fail -> Pending
_STATUS_RANK = {RESULT_PASS: 2, RESULT_FAIL: 1, RESULT_PENDING: 0}


class ResultManager:
    UPDATABLE_FIELDS = ("grade_fe", "grade_re", "status")

    def __init__(self, student_manager: StudentManager) -> None:
        self._student_manager = student_manager
        self._results: List[Result] = []

    def __len__(self) -> int:
        return len(self._results)

    # ---- truy vấn cơ bản ----------------------------------------------------
    @staticmethod
    def _key(student_id: str, course_id: str) -> Tuple[str, str]:
        return (str(student_id).strip().upper(), str(course_id).strip().upper())

    def find_result(self, student_id: str, course_id: str) -> Optional[Result]:
        key = self._key(student_id, course_id)
        return next((r for r in self._results if r.key == key), None)

    def get_result(self, student_id: str, course_id: str) -> Result:
        result = self.find_result(student_id, course_id)
        if result is None:
            sid, cid = self._key(student_id, course_id)
            raise NotFoundError(f"No result found for student '{sid}' in course '{cid}'.")
        return result

    def find_course_info(self, course_id: str) -> Optional[Tuple[str, int]]:
        """Nếu môn đã từng được nhập, trả về (course_name, credits) để gợi ý mặc định."""
        cid = str(course_id).strip().upper()
        match = next((r for r in self._results if r.course_id == cid), None)
        return (match.course_name, match.credits) if match else None

    def get_all(self) -> List[Result]:
        return sorted(self._results, key=lambda r: r.key)

    # ---- chức năng yêu cầu --------------------------------------------------
    def add_result(self, result: Result) -> None:
        """Thêm điểm môn học; sinh viên phải tồn tại và mỗi (student, course) chỉ có 1 dòng."""
        if not self._student_manager.exists(result.student_id):
            raise NotFoundError(f"Student '{result.student_id}' does not exist.")
        if self.find_result(result.student_id, result.course_id) is not None:
            raise DuplicateError(
                f"Student '{result.student_id}' already has a result for "
                f"course '{result.course_id}'. Use the update function instead."
            )
        self._results.append(result)

    def update_result(self, student_id: str, course_id: str, **changes: Any) -> Result:
        """Cập nhật grade_fe / grade_re / status theo (student_id, course_id).

        Đổi điểm sẽ tự tính lại status; nếu truyền cả status thì status thủ công được ưu tiên.
        """
        unknown = set(changes) - set(self.UPDATABLE_FIELDS)
        if unknown:
            raise ValidationError(f"Cannot update field(s): {', '.join(sorted(unknown))}.")

        current = self.get_result(student_id, course_id)
        candidate = copy.copy(current)          # sửa trên bản sao để đảm bảo toàn vẹn
        if "grade_fe" in changes or "grade_re" in changes:
            candidate.set_grades(
                changes.get("grade_fe", current.grade_fe),
                changes.get("grade_re", current.grade_re),
            )
        if "status" in changes:
            candidate.status = changes["status"]
        self._results[self._results.index(current)] = candidate
        return candidate

    def find_by_student(self, student_id: str) -> List[Result]:
        """Tìm các môn đã đăng ký / có điểm của một sinh viên."""
        sid = str(student_id).strip().upper()
        return sorted(filter(lambda r: r.student_id == sid, self._results), key=lambda r: r.key)

    def sorted_by_status(self, results: Optional[List[Result]] = None,
                         descending: bool = True) -> List[Result]:
        """Sắp xếp theo status giảm dần (Pass -> Fail -> Pending); đồng hạng thì theo mã."""
        source = self._results if results is None else results
        by_key = sorted(source, key=lambda r: r.key)
        return sorted(by_key, key=lambda r: _STATUS_RANK[r.status], reverse=descending)

    def get_passed_results(self) -> List[Result]:
        return list(filter(lambda r: r.is_passed, self.get_all()))

    def get_passed_student_ids(self) -> List[str]:
        return sorted({r.student_id for r in self._results if r.is_passed})

    def summary(self, student_id: str) -> Dict[str, Any]:
        """Thống kê nhanh cho một sinh viên (số môn, tín chỉ, điểm trung bình có trọng số)."""
        results = self.find_by_student(student_id)
        graded = [r for r in results if r.final_grade is not None]
        graded_credits = sum(r.credits for r in graded)
        average = (
            sum(r.final_grade * r.credits for r in graded) / graded_credits  # type: ignore[operator]
            if graded_credits else None
        )
        return {
            "courses": len(results),
            "passed": sum(1 for r in results if r.is_passed),
            "total_credits": sum(r.credits for r in results),
            "passed_credits": sum(r.credits for r in results if r.is_passed),
            "average": average,
        }

    # ---- file I/O -----------------------------------------------------------
    def save_to_file(self, path: PathLike) -> None:
        write_records(path, Result.FIELDS, (r.to_record() for r in self.get_all()))

    def load_from_file(self, path: PathLike) -> Tuple[int, List[str]]:
        """Nạp kết quả từ file (nên nạp danh sách sinh viên trước).

        Bỏ qua dòng sai, trùng khoá hoặc trỏ tới sinh viên không tồn tại.
        """
        rows = read_records(path)
        loaded: List[Result] = []
        seen = set()
        errors: List[str] = []
        for line_no, values in rows:
            try:
                result = Result.from_record(values)
                if not self._student_manager.exists(result.student_id):
                    raise NotFoundError(f"Student '{result.student_id}' does not exist.")
                if result.key in seen:
                    raise DuplicateError(
                        f"Duplicate result for {result.student_id} / {result.course_id}."
                    )
                seen.add(result.key)
                loaded.append(result)
            except StudentManagementError as exc:
                errors.append(f"Line {line_no}: {exc}")
        self._results = loaded
        return len(loaded), errors
