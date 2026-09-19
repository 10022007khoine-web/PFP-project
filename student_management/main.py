"""Điểm khởi chạy của chương trình: python main.py"""
from __future__ import annotations

import sys

from ui.menu import ConsoleApp


def main() -> None:
    # Đảm bảo console in được tiếng Việt có dấu (Windows / terminal cũ)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    ConsoleApp().run()


if __name__ == "__main__":
    main()
