"""StudentManager: quản lý danh sách sinh viên (lưu bằng dict: student_id -> Student)."""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

from models.student import Student
from utils import validators as v
from utils.constants import STATUS_ACTIVE, STUDENT_ID_DIGITS, STUDENT_ID_PREFIX
from utils.exceptions import DuplicateError, NotFoundError, StudentManagementError
from utils.file_handler import PathLike, read_records, write_records


class StudentManager:
    def __init__(self) -> None:
        self._students: Dict[str, Student] = {}

    def __len__(self) -> int:
        return len(self._students)

    # ---- truy vấn cơ bản ----------------------------------------------------
    @staticmethod
    def _normalize_id(student_id: str) -> str:
        return str(student_id).strip().upper()

    def exists(self, student_id: str) -> bool:
        return self._normalize_id(student_id) in self._students

    def get_student(self, student_id: str) -> Student:
        key = self._normalize_id(student_id)
        try:
            return self._students[key]
        except KeyError:
            raise NotFoundError(f"Student '{key}' was not found.") from None

    def get_all(self) -> List[Student]:
        return sorted(self._students.values(), key=lambda student: student.student_id)

    # ---- chức năng yêu cầu --------------------------------------------------
    def add_student(self, student: Student) -> None:
        """Thêm sinh viên mới; student_id phải là duy nhất."""
        if student.student_id in self._students:
            raise DuplicateError(f"Student ID '{student.student_id}' already exists.")
        self._students[student.student_id] = student

    def update_student(self, student_id: str, **changes: Any) -> Student:
        """Cập nhật thông tin theo student_id.

        Sửa trên bản sao rồi mới thay thế: nếu một trường sai thì không trường nào bị đổi.
        """
        current = self.get_student(student_id)
        candidate = copy.copy(current)
        candidate.update(**changes)
        self._students[current.student_id] = candidate
        return candidate

    def filter_by_class(self, class_name: str) -> List[Student]:
        key = v.validate_class_name(class_name)
        return list(filter(lambda s: s.class_name == key, self.get_all()))

    def filter_by_status(self, status: str) -> List[Student]:
        key = v.validate_student_status(status)
        return list(filter(lambda s: s.status == key, self.get_all()))

    def get_active_students(self) -> List[Student]:
        return self.filter_by_status(STATUS_ACTIVE)

    # ---- tiện ích -----------------------------------------------------------
    def next_student_id(self) -> str:
        """Gợi ý mã tiếp theo: SE + số lớn nhất hiện có + 1."""
        prefix_len = len(STUDENT_ID_PREFIX)
        numbers = [
            int(sid[prefix_len:])
            for sid in self._students
            if sid.startswith(STUDENT_ID_PREFIX) and sid[prefix_len:].isdigit()
        ]
        return f"{STUDENT_ID_PREFIX}{max(numbers, default=0) + 1:0{STUDENT_ID_DIGITS}d}"

    def get_classes(self) -> List[str]:
        return sorted({student.class_name for student in self._students.values()})

    # ---- file I/O -----------------------------------------------------------
    def save_to_file(self, path: PathLike) -> None:
        write_records(path, Student.FIELDS, (s.to_record() for s in self.get_all()))

    def load_from_file(self, path: PathLike) -> Tuple[int, List[str]]:
        """Nạp dữ liệu từ file và thay thế danh sách hiện tại.

        Dòng lỗi bị bỏ qua và được báo lại. Trả về (số_sinh_viên_nạp_được, danh_sách_lỗi).
        Nếu không đọc được file, ném FileDataError và giữ nguyên dữ liệu cũ.
        """
        rows = read_records(path)
        loaded: Dict[str, Student] = {}
        errors: List[str] = []
        for line_no, values in rows:
            try:
                student = Student.from_record(values)
                if student.student_id in loaded:
                    raise DuplicateError(f"Duplicate student ID '{student.student_id}'.")
                loaded[student.student_id] = student
            except StudentManagementError as exc:
                errors.append(f"Line {line_no}: {exc}")
        self._students = loaded
        return len(loaded), errors
