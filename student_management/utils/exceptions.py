"""Các exception tự định nghĩa của ứng dụng."""
from __future__ import annotations


class StudentManagementError(Exception):
    """Lỗi gốc của ứng dụng - bắt lớp này sẽ bắt được mọi lỗi nghiệp vụ."""


class ValidationError(StudentManagementError):
    """Dữ liệu nhập vào không hợp lệ."""


class DuplicateError(StudentManagementError):
    """Dữ liệu bị trùng (student_id hoặc cặp student_id + course_id)."""


class NotFoundError(StudentManagementError):
    """Không tìm thấy sinh viên / kết quả học tập."""


class FileDataError(StudentManagementError):
    """Lỗi đọc / ghi file dữ liệu."""


class OperationCancelled(Exception):
    """Người dùng gõ /q để huỷ thao tác đang nhập (không phải lỗi)."""
