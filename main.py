import sys

def main():
    pick= -1
    while pick != 0:
        try:
            pick = int(input("Enter your choice function: "))
        except Exception:
            print("(!) Invalid choice. Please try again.")
            continue 
        try:
            if pick == 1:
                #(1) Add Student
                print("You have selected function 1")
                name = str(input("Enter name student: "))
                id = str(input("Enter id student: "))
                birth = str(input("Enter birth student (YYYY/MM/DD): "))
                phone = str(input("Enter phone student: "))
                gender = str(input("Enter gender student (male/female): "))
                class_name = str(input("Enter class student: "))
                email = str(input("Enter email student: "))
                status = str(input("Enter status student ( Active / Inactive / Graduated): "))
            elif pick == 2:
                #(2) Add Course Student
                print("You have selected function 2")
                checkid= str(input("Enter id student: "))
                if checkid == id:
                    course_name = str(input("Enter course name: "))
                    course_id = str(input("Enter course id: "))
                    semester = str(input("Enter semester (EX: Fall2026): "))
                    credits = int(input("Enter credits: "))
                    grade_FE = input("Enter grade FE (ex: 6.7 or blank if not yet graded): ")
                    grade_RE = input("Enter grade PE (ex: 3.6 or blank if not yet graded): ")
                    status = str(input("Enter status course (Pass/Fail): "))
                else:
                    print("(!) Student not found.")
            elif pick == 3:
                #(3) Update Student
                print("You have selected function 3")
                checkid= str(input("Enter id student: "))
                if checkid == id:
                    name = str(input("Enter new name student: "))
                    birth = str(input("Enter new birth student (YYYY/MM/DD): "))
                    phone = str(input("Enter new phone student: "))
                    gender = str(input("Enter new gender student (male/female): "))
                    class_name = str(input("Enter new class student: "))
                    email = str(input("Enter new email student: "))
                    status = str(input("Enter new status student ( Active / Inactive / Graduated): "))
                else:
                    print("(!) Student not found.")
            elif pick == 0:
                break
            else:
                print("(!) Invalid choice. Please try again.")
        except Exception:
            print("(!) Invalid input. Please try again.")
            continue
    print(f"{name} has been added successfully.")
    print(f"Student ID: {id}")
    print(f"Birth: {birth}")
    print(f"Phone: {phone}")
if __name__ == "__main__":
    main()
