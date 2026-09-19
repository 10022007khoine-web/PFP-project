"""Package services: logic nghiệp vụ quản lý sinh viên và kết quả học tập."""
from .result_manager import ResultManager
from .student_manager import StudentManager

__all__ = ["StudentManager", "ResultManager"]
