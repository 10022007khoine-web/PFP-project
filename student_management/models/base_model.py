"""Lớp cha trừu tượng cho mọi model - thể hiện tính kế thừa (inheritance)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Sequence


class BaseModel(ABC):
    """Model nào cũng phải biết tự chuyển thành / tạo lại từ một dòng text."""

    FIELDS: tuple = ()  # tên các thuộc tính, theo đúng thứ tự lưu trong file

    @abstractmethod
    def to_record(self) -> List[str]:
        """Chuyển object thành danh sách chuỗi để ghi ra file."""

    @classmethod
    @abstractmethod
    def from_record(cls, values: Sequence[str]) -> "BaseModel":
        """Tạo object từ danh sách chuỗi đọc từ file (có thể ném ValidationError)."""

    def to_dict(self) -> Dict[str, Any]:
        return {name: getattr(self, name) for name in self.FIELDS}
