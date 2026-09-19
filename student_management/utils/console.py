"""Tiện ích nhập / xuất trên console: hỏi có kiểm tra, xác nhận, in bảng."""
from __future__ import annotations

from typing import Any, Callable, Optional, Sequence

from .exceptions import OperationCancelled, ValidationError

CANCEL_KEYWORD = "/q"


def ask(
    prompt: str,
    validator: Optional[Callable[[str], Any]] = None,
    *,
    default: Any = None,
    allow_blank: bool = False,
) -> Any:
    """Hỏi lại cho đến khi nhập hợp lệ.

    - default: nhấn Enter sẽ dùng giá trị mặc định.
    - allow_blank: nhấn Enter trả về None (không qua validator).
    - Gõ /q để huỷ thao tác (ném OperationCancelled).
    """
    hint = f" [{default}]" if default not in (None, "") else ""
    while True:
        raw = input(f"  {prompt}{hint}: ").strip()
        if raw.lower() == CANCEL_KEYWORD:
            raise OperationCancelled()
        if not raw:
            if default not in (None, ""):
                raw = str(default)
            elif allow_blank:
                return None
            elif validator is None:
                print("  [!] This field is required.")
                continue
        try:
            return validator(raw) if validator else raw
        except ValidationError as exc:
            print(f"  [!] {exc}")


def confirm(prompt: str, default: bool = False) -> bool:
    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        raw = input(f"  {prompt}{suffix}: ").strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Please answer y or n.")


def print_header(title: str, width: int = 60) -> None:
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> None:
    """In bảng ASCII, độ rộng cột tự co giãn theo nội dung."""
    str_rows = [[str(cell) for cell in row] for row in rows]
    widths = [
        max([len(header)] + [len(row[index]) for row in str_rows])
        for index, header in enumerate(headers)
    ]
    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(cells: Sequence[str]) -> str:
        return "| " + " | ".join(cell.ljust(width) for cell, width in zip(cells, widths)) + " |"

    print(separator)
    print(format_row(list(headers)))
    print(separator)
    for row in str_rows:
        print(format_row(row))
    print(separator)
