"""Package models: các lớp dữ liệu (Student, Result)."""
from .base_model import BaseModel
from .result import Result
from .student import Student

__all__ = ["BaseModel", "Student", "Result"]
