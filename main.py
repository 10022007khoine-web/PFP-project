import sys
from display import display
def main():
    dis=display()
    pick= -1
    a=[]
    while pick != 0:
        dis.show_menu()
        try:
            pick = dis.read_int("Enter your choice function: ")
        except Exception:
            print("(!) Invalid choice. Please try again.")
            continue 
        try:
            if pick == 1:
                #(1) Add Student
                print("You have selected function 1")
                student_id = dis.read_str("Enter id student: ")
                full_name = dis.read_str("Enter name student: ")
                date_of_birth = dis.read_str("Enter birth student (YYYY/MM/DD): ")
                gender = dis.read_gender("Enter gender student (male/female): ")
                class_name = dis.read_str("Enter class student: ")
                phone = dis.read_str("Enter phone student: ")
                email = dis.read_str("Enter email student: ")
                status = dis.read_str("Enter status student ( active / inactive / graduated): ")
                a.append((full_name, student_id, date_of_birth, gender, class_name, phone, email, status))
            elif pick == 2:
                #(2) Add Course Student
                print("You have selected function 2")
                checkid= dis.read_str("Enter id student: ")
                if checkid == student_id:
                    course_id = dis.read_str("Enter course id: ")
                    course_name = dis.read_str("Enter course name: ")
                    semester = dis.read_str("Enter semester (EX: Fall2026): ")
                    credits = dis.read_int("Enter credits: ")
                    grade_FE = dis.read_str("Enter grade FE (ex: 6.7 or blank if not yet graded): ")
                    grade_RE = dis.read_str("Enter grade PE (ex: 3.6 or blank if not yet graded): ")
                    status_ok = dis.read_str("Enter status course (Pass/Fail): ")
                else:
                    print("(!) Student not found.")
            elif pick == 3:
                #(3) Update Student
                print("You have selected function 3")
                checkid= dis.read_str("Enter id student: ")
                if checkid == student_id:
                    phone = dis.read_str("Enter new phone student: ")
                    class_name = dis.read_str("Enter new class student: ")
                    email = dis.read_str("Enter new email student: ")
                    status = dis.read_str("Enter new status student ( Active / Inactive / Graduated): ")
                else:
                    print("(!) Student not found.")
            elif pick == 4:
                #(4) Update Mark Student
                print("You have selected function 4")
                checkid = dis.read_str("Enter id student: ")
                checkcourseid = dis.read_str("Enter id course: ")
                if checkid == student_id and checkcourseid == course_id:
                    grade_FE = dis.read_str("Enter new grade FE (ex: 6.7 or blank if not yet graded): ")
                    grade_RE = dis.read_str("Enter new grade PE (ex: 3.6 or blank if not yet graded): ")
                else:
                    print("(!) Student or course not found.")
            elif pick == 5:
                #(5) Search Student by Student ID
                print("You have selected function 5")
                checkid= dis.read_str("Enter id student: ")
                if checkid == student_id:
                    print(f"Student ID: {student_id}")
                    print(f"Full Name: {full_name}")
                    print(f"Birth: {date_of_birth}")
                    print(f"Gender: {gender}")
                    print(f"Class: {class_name}")
                    print(f"Phone: {phone}")
                    print(f"Email: {email}")
                    print(f"Status: {status}")
                else:
                    print("(!) Student not found.") 
            elif pick == 6:
                #(6) Filter Student by Mark
                print("You have selected function 6")
                print("1/ Filter grades in ascending order")
                print("2/ Filter grades in descending order")
                filter_choice = dis.read_int("Enter your choice: ")
                if filter_choice == 1:
                    print("You have selected to filter grades in ascending order")
                    # Implement the logic to filter grades in ascending order
                elif filter_choice == 2:
                    print("You have selected to filter grades in descending order")
                    # Implement the logic to filter grades in descending order
                else:
                    print("(!) Invalid choice. Please try again.")
            elif pick == 7:
                #(7) Print Status Student
                print("You have selected function 7")
                print("--- Student Status ---")
                # Print list status of student
            elif pick == 0:
                break
            else:
                print("(!) Invalid choice. Please try again.")
        except Exception:
            print("(!) Invalid input. Please try again.")
            continue
    print(f"{full_name} has been added successfully.")
    print(f"Student ID: {student_id}")
    print(f"Birth: {date_of_birth}")
    print(f"Phone: {phone}")
    print(a)

if __name__ == "__main__":
    main()
