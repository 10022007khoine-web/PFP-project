"""Giao diện console: hệ thống menu tương tác với người dùng."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Sequence, Tuple

from models.result import Result
from models.student import Student
from services.result_manager import ResultManager
from services.student_manager import StudentManager
from utils import validators as v
from utils.console import ask, confirm, print_header, print_table
from utils.constants import PASS_SCORE, RESULT_FILE, STATUS_ACTIVE, STUDENT_FILE
from utils.exceptions import (
    FileDataError,
    OperationCancelled,
    StudentManagementError,
    ValidationError,
)

_CLEAR = object()  # đánh dấu "xoá điểm" khi cập nhật (người dùng gõ x)

STUDENT_HEADERS = ["ID", "Full name", "Date of birth", "Gender", "Class", "Phone", "Email", "Status"]
MenuItem = Tuple[str, Callable[[], None]]


def _grade_text(grade) -> str:
    return "-" if grade is None else f"{grade:.1f}"


def _grade_or_clear(value: str):
    return _CLEAR if value.strip().lower() == "x" else v.validate_grade(value)


class ConsoleApp:
    def __init__(self, student_file=STUDENT_FILE, result_file=RESULT_FILE) -> None:
        self.student_file = Path(student_file)
        self.result_file = Path(result_file)
        self.students = StudentManager()
        self.results = ResultManager(self.students)
        self._dirty = False  # True nếu có thay đổi chưa lưu

    # ============================================================== chạy app ==
    def run(self) -> None:
        print_header("STUDENT MANAGEMENT SYSTEM")
        print("  PFP191 - Programming Fundamentals with Python")
        print("  Tip: type /q at any prompt to cancel the current operation.")
        try:
            self._startup_load()
            self._run_menu(
                "MAIN MENU",
                [
                    ("Student management", self._student_menu),
                    ("Result management", self._result_menu),
                    ("File handling (save / load)", self._file_menu),
                ],
                back_label="Exit",
            )
        except (KeyboardInterrupt, EOFError):
            print("\n  Interrupted.")
        self._on_exit()

    def _run_menu(self, title: str, items: Sequence[MenuItem], back_label: str = "Back") -> None:
        while True:
            print_header(title)
            for number, (label, _) in enumerate(items, start=1):
                print(f"  {number}. {label}")
            print(f"  0. {back_label}")
            choice = input("\n  Your choice: ").strip()
            if choice == "0":
                return
            if choice.isdigit() and 1 <= int(choice) <= len(items):
                self._safe_call(items[int(choice) - 1][1])
            else:
                print("  [!] Invalid choice, please try again.")

    @staticmethod
    def _safe_call(handler: Callable[[], None]) -> None:
        """Bắt lỗi ở biên giao diện để chương trình không bị thoát đột ngột."""
        try:
            handler()
        except OperationCancelled:
            print("  Cancelled.")
        except StudentManagementError as exc:
            print(f"  [!] {exc}")
        except EOFError:
            raise
        except Exception as exc:  # noqa: BLE001 - lưới an toàn cuối cùng
            print(f"  [!] Unexpected error: {exc}")

    def _on_exit(self) -> None:
        try:
            if self._dirty and confirm("You have unsaved changes. Save before exiting?", True):
                self._save_all()
        except (EOFError, KeyboardInterrupt):
            print("\n  Unsaved changes were discarded.")
        except StudentManagementError as exc:
            print(f"  [!] {exc}")
        print("  Goodbye!")

    # ================================================================ menus ===
    def _student_menu(self) -> None:
        self._run_menu(
            "STUDENT MANAGEMENT",
            [
                ("Add a new student", self._add_student),
                ("Update student information", self._update_student),
                ("Filter students by class", self._filter_by_class),
                ("Filter students by status", self._filter_by_status),
                ("Display active students", self._display_active),
                ("Display all students", self._display_all_students),
            ],
        )

    def _result_menu(self) -> None:
        self._run_menu(
            "RESULT MANAGEMENT",
            [
                ("Add a student's course grade", self._add_result),
                ("Update grade / status of a course", self._update_result),
                ("Search enrollments by student ID", self._search_enrollments),
                ("Display exam results (sorted by status, descending)", self._display_results),
                ("Display students with a 'Pass' result", self._display_passed),
            ],
        )

    def _file_menu(self) -> None:
        self._run_menu(
            "FILE HANDLING",
            [
                ("Save data to files", self._save_all),
                ("Load data from files", self._manual_load),
            ],
        )

    # ============================================================= students ===
    def _add_student(self) -> None:
        def new_id(value: str) -> str:
            student_id = v.validate_student_id(value)
            if self.students.exists(student_id):
                raise ValidationError(f"Student ID '{student_id}' already exists.")
            return student_id

        print("\n  --- Add a new student ---")
        student_id = ask("Student ID", new_id, default=self.students.next_student_id())
        student = Student(
            student_id=student_id,
            full_name=ask("Full name", v.validate_full_name),
            date_of_birth=ask("Date of birth (dd/mm/yyyy)", v.validate_date_of_birth),
            gender=ask("Gender (Male/Female)", v.validate_gender),
            class_name=ask("Class (e.g. SE1901)", v.validate_class_name),
            phone=ask("Phone", v.validate_phone),
            email=ask("Email", v.validate_email),
            status=ask("Status (Active/Inactive/Graduated)", v.validate_student_status,
                       default=STATUS_ACTIVE),
        )
        self.students.add_student(student)
        self._dirty = True
        print(f"  Student added successfully: {student}")

    def _update_student(self) -> None:
        print("\n  --- Update student information ---")
        student_id = ask("Student ID to update", v.validate_student_id)
        student = self.students.get_student(student_id)
        print(f"  Current: {student}")
        print("  Press Enter to keep the current value.")

        specs = [
            ("full_name", "Full name", v.validate_full_name),
            ("date_of_birth", "Date of birth (dd/mm/yyyy)", v.validate_date_of_birth),
            ("gender", "Gender (Male/Female)", v.validate_gender),
            ("class_name", "Class", v.validate_class_name),
            ("phone", "Phone", v.validate_phone),
            ("email", "Email", v.validate_email),
            ("status", "Status (Active/Inactive/Graduated)", v.validate_student_status),
        ]
        changes = {
            field: ask(label, validator, default=getattr(student, field))
            for field, label, validator in specs
        }
        changes = {k: val for k, val in changes.items() if val != getattr(student, k)}
        if not changes:
            print("  No changes made.")
            return
        updated = self.students.update_student(student_id, **changes)
        self._dirty = True
        print(f"  Updated successfully: {updated}")

    def _show_students(self, students: List[Student], title: str) -> None:
        print(f"\n  {title}")
        if not students:
            print("  No students found.")
            return
        rows = [[s.student_id, s.full_name, s.date_of_birth, s.gender, s.class_name,
                 s.phone, s.email, s.status] for s in students]
        print_table(STUDENT_HEADERS, rows)
        print(f"  Total: {len(students)} student(s)")

    def _filter_by_class(self) -> None:
        classes = self.students.get_classes()
        if classes:
            print(f"  Available classes: {', '.join(classes)}")
        class_name = ask("Class name", v.validate_class_name)
        self._show_students(self.students.filter_by_class(class_name),
                            f"Students in class {class_name}:")

    def _filter_by_status(self) -> None:
        status = ask("Status (Active/Inactive/Graduated)", v.validate_student_status)
        self._show_students(self.students.filter_by_status(status),
                            f"Students with status '{status}':")

    def _display_active(self) -> None:
        self._show_students(self.students.get_active_students(), "Active students:")

    def _display_all_students(self) -> None:
        self._show_students(self.students.get_all(), "All students:")

    # ============================================================== results ===
    def _add_result(self) -> None:
        print("\n  --- Add a student's course grade ---")
        student_id = ask("Student ID", v.validate_student_id)
        student = self.students.get_student(student_id)
        print(f"  Student: {student.full_name} ({student.class_name})")

        course_id = ask("Course ID (e.g. PFP191)", v.validate_course_id)
        if self.results.find_result(student_id, course_id) is not None:
            print(f"  [!] {student.student_id} already has a result for {course_id}. "
                  "Use 'Update grade / status' instead.")
            return

        known = self.results.find_course_info(course_id)  # gợi ý tên môn / số tín chỉ
        course_name = ask("Course name", v.validate_course_name,
                          default=known[0] if known else None)
        semester = ask("Semester (e.g. Fall2026)", v.validate_semester)
        credits = ask("Credits", v.validate_credits, default=known[1] if known else None)
        grade_fe = ask("Grade FE (0-10, Enter if not graded yet)", v.validate_grade,
                       allow_blank=True)
        grade_re = None
        if grade_fe is not None and grade_fe < PASS_SCORE:
            grade_re = ask("Grade RE (0-10, Enter if no retake yet)", v.validate_grade,
                           allow_blank=True)

        result = Result(student.student_id, course_id, course_name, semester, credits,
                        grade_fe, grade_re)
        self.results.add_result(result)
        self._dirty = True
        print(f"  Result added: {result}")

    def _update_result(self) -> None:
        print("\n  --- Update grade / status of a course ---")
        student_id = ask("Student ID", v.validate_student_id)
        course_id = ask("Course ID", v.validate_course_id)
        result = self.results.get_result(student_id, course_id)
        print(f"  Current: {result}")
        print("  Press Enter to keep a value, type x to clear a grade.")

        changes = {}
        grade_fe = ask("New grade FE (0-10)", _grade_or_clear, allow_blank=True)
        if grade_fe is not None:
            changes["grade_fe"] = None if grade_fe is _CLEAR else grade_fe
        grade_re = ask("New grade RE (0-10)", _grade_or_clear, allow_blank=True)
        if grade_re is not None:
            changes["grade_re"] = None if grade_re is _CLEAR else grade_re
        status = ask("Set status manually (Pass/Fail/Pending), Enter = automatic",
                     v.validate_result_status, allow_blank=True)
        if status is not None:
            changes["status"] = status

        if not changes:
            print("  No changes made.")
            return
        updated = self.results.update_result(student_id, course_id, **changes)
        self._dirty = True
        print(f"  Updated successfully: {updated}")

    def _print_results_table(self, results: List[Result], show_name: bool) -> None:
        headers = ["Student ID"] + (["Student name"] if show_name else []) + [
            "Course", "Course name", "Semester", "Credits", "FE", "RE", "Status"]
        rows = []
        for r in results:
            name = [self.students.get_student(r.student_id).full_name] if show_name else []
            rows.append([r.student_id] + name + [
                r.course_id, r.course_name, r.semester, r.credits,
                _grade_text(r.grade_fe), _grade_text(r.grade_re), r.status])
        print_table(headers, rows)

    def _print_summary(self, student_id: str) -> None:
        s = self.results.summary(student_id)
        average = "N/A" if s["average"] is None else f"{s['average']:.2f}"
        print(f"  Courses: {s['courses']} | Passed: {s['passed']} | "
              f"Credits passed: {s['passed_credits']}/{s['total_credits']} | "
              f"Weighted average: {average}")

    def _search_enrollments(self) -> None:
        student_id = ask("Student ID", v.validate_student_id)
        student = self.students.get_student(student_id)
        results = self.results.find_by_student(student_id)
        print(f"\n  Enrollments of {student.student_id} - {student.full_name} ({student.class_name}):")
        if not results:
            print("  No enrollments found.")
            return
        self._print_results_table(results, show_name=False)
        self._print_summary(student.student_id)

    def _display_results(self) -> None:
        student_id = ask("Student ID (Enter to show all students)", v.validate_student_id,
                         allow_blank=True)
        if student_id is not None:
            student = self.students.get_student(student_id)
            results = self.results.sorted_by_status(self.results.find_by_student(student_id))
            print(f"\n  Exam results of {student.student_id} - {student.full_name} "
                  "(sorted by status, descending):")
            if not results:
                print("  No results found.")
                return
            self._print_results_table(results, show_name=False)
            self._print_summary(student.student_id)
        else:
            results = self.results.sorted_by_status()
            print("\n  All exam results (sorted by status, descending):")
            if not results:
                print("  No results found.")
                return
            self._print_results_table(results, show_name=True)
            print(f"  Total: {len(results)} result(s)")

    def _display_passed(self) -> None:
        passed = self.results.get_passed_results()
        print("\n  Students with a 'Pass' result (FE >= 5, or FE < 5 and RE >= 5):")
        if not passed:
            print("  No passed results found.")
            return
        self._print_results_table(passed, show_name=True)
        print(f"  {len(self.results.get_passed_student_ids())} student(s), "
              f"{len(passed)} passed course(s)")

    # ================================================================= files ===
    def _save_all(self) -> None:
        self.students.save_to_file(self.student_file)
        self.results.save_to_file(self.result_file)
        self._dirty = False
        print(f"  Saved {len(self.students)} student(s) to {self.student_file.name} and "
              f"{len(self.results)} result(s) to {self.result_file.name}.")

    def _load_all(self) -> None:
        """Nạp sinh viên trước, rồi kết quả (vì kết quả cần tham chiếu tới sinh viên)."""
        sources = (
            ("student(s)", self.student_file, self.students.load_from_file),
            ("result(s)", self.result_file, self.results.load_from_file),
        )
        for label, path, loader in sources:
            if not path.exists():
                print(f"  [i] {path.name} not found - nothing loaded for {label}.")
                continue
            count, errors = loader(path)
            print(f"  Loaded {count} {label} from {path.name}.")
            for message in errors[:10]:
                print(f"    [!] {message}")
            if len(errors) > 10:
                print(f"    ... and {len(errors) - 10} more problem(s).")
        self._dirty = False

    def _startup_load(self) -> None:
        try:
            self._load_all()
        except FileDataError as exc:
            print(f"  [!] {exc}")

    def _manual_load(self) -> None:
        if self._dirty and not confirm("Unsaved changes will be lost. Continue?"):
            print("  Load cancelled.")
            return
        self._load_all()
