# Student Management System (PFP191 – Topic 4)

Ứng dụng console quản lý **sinh viên** và **kết quả học tập**, viết bằng Python thuần (chỉ dùng thư viện chuẩn, Python ≥ 3.8).

## Chạy chương trình

```bash
python main.py                 # chạy ứng dụng (tự nạp data/students.txt và data/results.txt nếu có)
python -m unittest discover -v # chạy 26 unit test
```

Gõ `/q` ở bất kỳ câu hỏi nhập liệu nào để huỷ thao tác hiện tại.

## Cấu trúc project

```
student_management/
├── main.py                  # điểm khởi chạy
├── models/                  # lớp dữ liệu (OOP)
│   ├── base_model.py        #   BaseModel (ABC) – lớp cha: to_record()/from_record()
│   ├── student.py           #   Student  – private attr + @property + __str__
│   └── result.py            #   Result   – luật Pass/Fail, tối đa 2 lần thi
├── services/                # logic nghiệp vụ
│   ├── student_manager.py   #   StudentManager (dict: student_id -> Student)
│   └── result_manager.py    #   ResultManager  (list[Result])
├── utils/                   # tiện ích dùng chung
│   ├── constants.py         #   hằng số, đường dẫn file
│   ├── exceptions.py        #   exception tự định nghĩa
│   ├── validators.py        #   kiểm tra & chuẩn hoá dữ liệu nhập
│   ├── file_handler.py      #   đọc/ghi file .txt
│   └── console.py           #   ask()/confirm()/print_table()
├── ui/menu.py               # giao diện CLI (ConsoleApp)
├── data/                    # students.txt, results.txt (dữ liệu mẫu)
└── tests/                   # unit test (unittest)
```

Luồng phụ thuộc một chiều: `ui → services → models → utils`.

## Đối chiếu yêu cầu đề bài

| Yêu cầu | Vị trí |
|---|---|
| Thêm / cập nhật SV theo `student_id`, lọc theo lớp / trạng thái, hiển thị SV Active | `StudentManager` + menu *Student management* |
| `student_id` không trùng | `StudentManager.add_student` → `DuplicateError` |
| Thêm điểm, cập nhật điểm/status theo `student_id` + `course_id` | `ResultManager.add_result / update_result` |
| Tìm enrollments theo student ID | `ResultManager.find_by_student` |
| Hiển thị kết quả, sắp xếp status giảm dần | `ResultManager.sorted_by_status` |
| Danh sách Pass: `FE >= 5` hoặc (`FE < 5` và `RE >= 5`) | `Result.calculate_status`, `get_passed_results` |
| Tối đa 2 lần thi mỗi môn | `Result.set_grades` (chỉ có FE và RE; RE chỉ nhập được khi FE < 5) |
| Lưu / nạp file .txt | `utils/file_handler.py`, `save_to_file / load_from_file` |
| OOP: constructor, encapsulation, inheritance | `BaseModel` → `Student`, `Result` |
| `__str__`, `@property` | `Student`, `Result` |
| Xử lý exception | `utils/exceptions.py`, bắt ở `ui/menu.py::_safe_call` |
| Hàm built-in | `sorted`, `filter`, `max`, `sum`, `any/all`, `enumerate`, `zip`, `next`, `set` |
| Packages `models/ services/ utils/` | có đủ (thêm `ui/` tách phần giao diện) |

## Định dạng file dữ liệu

M��i dòng một bản ghi, các trường cách nhau bằng `|`; dòng bắt đầu bằng `#` là chú thích.
Điểm để trống nghĩa là chưa chấm.

```
# student_id|full_name|date_of_birth|gender|class_name|phone|email|status
SE00001|Nguyen Van An|15/03/2005|Male|SE1901|0901234567|an.nguyen@fpt.edu.vn|Active

# student_id|course_id|course_name|semester|credits|grade_fe|grade_re|status
SE00001|MAD101|Discrete Mathematics|Fall2026|3|4.0|6.0|Pass
```

Khi nạp file, dòng sai định dạng / trùng khoá / trỏ tới sinh viên không tồn tại bị bỏ qua và được báo số dòng.
Ghi file dùng file tạm + `os.replace` để không làm hỏng dữ liệu cũ nếu ghi lỗi giữa chừng.

## Quy ước thiết kế (giả định khi đề bài chưa nói rõ)

- **Mã sinh viên**: 2 chữ cái + 5 số (`SE00001`, đúng ví dụ ở mục 1 của đề). Ví dụ `S001` ở mục 2 bị coi là không nhất quán nên không dùng.
- **Khoá của Result**: cặp (`student_id`, `course_id`) là duy nhất → việc "cập nhật theo student_id và course_id" luôn xác định đúng một dòng.
- **Status của Result**: tự tính từ điểm mỗi khi đổi điểm; vẫn cho phép đặt tay. Thêm giá trị **`Pending`** cho môn chưa có điểm FE (đề cho phép điểm để trống nhưng chỉ nêu Pass/Fail).
- **Sắp xếp giảm dần theo status**: thứ tự `Pass → Fail → Pending`.
- **Cập nhật an toàn**: sửa trên bản sao rồi mới thay thế; nếu một trường sai thì không trường nào bị đổi.
- **Thoát chương trình**: nếu còn thay đổi chưa lưu, chương trình hỏi có lưu hay không.
