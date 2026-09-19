"""Hằng số dùng chung cho toàn bộ project."""
from __future__ import annotations

from pathlib import Path

# ---- Đường dẫn dữ liệu ------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STUDENT_FILE = DATA_DIR / "students.txt"
RESULT_FILE = DATA_DIR / "results.txt"

# ---- Định dạng file .txt -----------------------------------------------------
ENCODING = "utf-8"
DELIMITER = "|"          # ký tự phân cách các trường trên mỗi dòng
COMMENT_PREFIX = "#"     # dòng bắt đầu bằng ký tự này bị bỏ qua khi đọc

# ---- Student -----------------------------------------------------------------
STUDENT_ID_PREFIX = "SE"
STUDENT_ID_DIGITS = 5
GENDERS = ("Male", "Female")
STATUS_ACTIVE = "Active"
STUDENT_STATUSES = (STATUS_ACTIVE, "Inactive", "Graduated")
MIN_AGE = 15
MAX_AGE = 100

# ---- Result ------------------------------------------------------------------
RESULT_PASS = "Pass"
RESULT_FAIL = "Fail"
RESULT_PENDING = "Pending"   # chưa có điểm FE
RESULT_STATUSES = (RESULT_PASS, RESULT_FAIL, RESULT_PENDING)
PASS_SCORE = 5.0
MAX_GRADE = 10.0
MIN_CREDITS = 1
MAX_CREDITS = 10
