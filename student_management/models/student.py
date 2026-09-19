"""Model Student: đóng gói (encapsulation) bằng thuộc tính private + @property."""
from __future__ import annotations

from typing import Any, List, Sequence

from utils import validators as v
from utils.constants import STATUS_ACTIVE
from utils.exceptions import ValidationError

from .base_model import BaseModel


class Student(BaseModel):
    FIELDS = (
        "student_id", "full_name", "date_of_birth", "gender",
        "class_name", "phone", "email", "status",
    )
    UPDATABLE_FIELDS = FIELDS[1:]  # student_id là khoá chính, không được sửa

    def __init__(
        self,
        student_id: str,
        full_name: str,
        date_of_birth: str,
        gender: str,
        class_name: str,
        phone: str,
        email: str,
        status: str = STATUS_ACTIVE,
    ) -> None:
        self._student_id = v.validate_student_id(student_id)
        # Các phép gán dưới đây đi qua setter nên luôn được validate
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.class_name = class_name
        self.phone = phone
        self.email = email
        self.status = status

    # ---- properties (student_id chỉ đọc) ------------------------------------
    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        self._full_name = v.validate_full_name(value)

    @property
    def date_of_birth(self) -> str:
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: str) -> None:
        self._date_of_birth = v.validate_date_of_birth(value)

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str) -> None:
        self._gender = v.validate_gender(value)

    @property
    def class_name(self) -> str:
        return self._class_name

    @class_name.setter
    def class_name(self, value: str) -> None:
        self._class_name = v.validate_class_name(value)

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = v.validate_phone(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = v.validate_email(value)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = v.validate_student_status(value)

    @property
    def is_active(self) -> bool:
        return self._status == STATUS_ACTIVE

    # ---- nghiệp vụ ----------------------------------------------------------
    def update(self, **changes: Any) -> None:
        """Cập nhật nhiều trường cùng lúc, ví dụ update(phone="0912345678")."""
        for name in changes:
            if name not in self.UPDATABLE_FIELDS:
                raise ValidationError(f"Field '{name}' cannot be updated.")
        for name, value in changes.items():
            setattr(self, name, value)

    # ---- chuyển đổi file ----------------------------------------------------
    def to_record(self) -> List[str]:
        return [str(getattr(self, name)) for name in self.FIELDS]

    @classmethod
    def from_record(cls, values: Sequence[str]) -> "Student":
        if len(values) != len(cls.FIELDS):
            raise ValidationError(
                f"Expected {len(cls.FIELDS)} fields but found {len(values)}."
            )
        return cls(*values)

    # ---- hiển thị -----------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"[{self._student_id}] {self._full_name} | {self._date_of_birth} | "
            f"{self._gender} | {self._class_name} | {self._phone} | "
            f"{self._email} | {self._status}"
        )

    def __repr__(self) -> str:
        return f"Student(student_id={self._student_id!r}, full_name={self._full_name!r})"
