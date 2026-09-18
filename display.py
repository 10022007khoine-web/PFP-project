class display:
    def show_menu(hey):
        #Function to display the main menu.
        print("\n--- Student Management System ---")
        print("============================================")
        print("1. Add Student")
        print("2. Add Course Student")
        print("3. Update Student")
        print("4. Update Mark Student")
        print("5. Search Student by Student ID")
        print("6. Sorted Student by Mark")
        print("7. Print Status Student")
        print("0. Exit")
        print("--------------------------------------------")
    def read_str(hey, code: str) -> str:
        #Function to read a string input from the user.
        return input(code).strip()
    def read_gender(hey, code: str) -> str:
        #Function to read gender input from the user, ensuring it's either 'male' or 'female'.
        while True:
            gender = input(code).strip().lower()
            if gender in ["male", "female"]:
                return gender
            print("(!) Invalid gender. Please enter 'male' or 'female'.")
    def read_int(hey, code: str) -> int:
        #Function to read an integer input from the user, ensuring it's a valid integer.
        while True:
            try:
                return int(input(code))
            except ValueError:
                print("(!) Invalid input. Please enter a valid integer.")
    def read_float(hey, code: str) -> float:
        #Function to read a float input from the user, ensuring it's a valid float.
        while True:
            try:
                return float(input(code))
            except ValueError:
                print("(!) Invalid input. Please enter a valid float.")
    def read_optional_float(hey, code: str):
        """Đọc điểm RE (Nhấn Enter để bỏ qua nếu chưa thi)"""
        val = input(code).strip()
        if not val or val == "-":
            return None
        try:
            return float(val)
        except ValueError:
            print("(!) Invalid input. Setting to None.")
            return None