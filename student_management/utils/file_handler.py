"""Đọc / ghi file .txt dạng bản ghi phân cách bằng ký tự '|'.

Định dạng:
    # student_id|full_name|...        <- dòng tiêu đề (bị bỏ qua khi đọc)
    SE00001|Nguyen Van An|...          <- mỗi dòng một bản ghi
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple, Union

from .constants import COMMENT_PREFIX, DELIMITER, ENCODING
from .exceptions import FileDataError

PathLike = Union[str, Path]


def write_records(path: PathLike, header: Sequence[str], records: Iterable[Sequence[str]]) -> None:
    """Ghi file an toàn: ghi ra file tạm rồi mới thay thế file thật."""
    path = Path(path)
    tmp_path = path.with_name(path.name + ".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_path, "w", encoding=ENCODING, newline="\n") as file:
            file.write(f"{COMMENT_PREFIX} {DELIMITER.join(header)}\n")
            for record in records:
                file.write(DELIMITER.join(record) + "\n")
        os.replace(tmp_path, path)
    except OSError as exc:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        raise FileDataError(f"Cannot write file '{path}': {exc}") from exc


def read_records(path: PathLike) -> List[Tuple[int, List[str]]]:
    """Trả về danh sách (số_dòng, [các trường]); bỏ qua dòng trống và dòng chú thích."""
    path = Path(path)
    try:
        with open(path, "r", encoding="utf-8-sig") as file:  # utf-8-sig: chịu được BOM
            lines = file.read().splitlines()
    except FileNotFoundError:
        raise FileDataError(f"File not found: '{path}'.") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise FileDataError(f"Cannot read file '{path}': {exc}") from exc

    records: List[Tuple[int, List[str]]] = []
    for line_no, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith(COMMENT_PREFIX):
            continue
        records.append((line_no, [field.strip() for field in line.split(DELIMITER)]))
    return records
