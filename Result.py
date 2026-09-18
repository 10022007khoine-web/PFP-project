class Result:
    def __init__(self, student_id, course_id, course_name, semester, credits, grade_fe:float, grade_re: float=None):
        self.student_id = student_id
        self.course_id = course_id
        self.course_name = course_name
        self.semester = semester
        self.credits = credits
        self.grade_fe = grade_fe
        self.grade_re = grade_re
    def get_status(self):
        if self.grade_fe >=5.0:
            return "Pass"
        else:
            if self.grade_re is not None and self.grade_re != "-" and self.grade_re >=5.0:
                return "Pass"
            else: 
                return "Fail"
    def display_result(self):
        fe_str = f"{self.grade_fe:.1f}"
        re_str = f"{self.grade_re:.1f}" if self.grade_re is not None else "-"
        status = self.get_status()
        print(f"Course ID: {self.course_id}, Course Name: {self.course_name} | Student ID: {self.student_id} | Semester: {self.semester} | Credits: {self.credits} | Grade FE: {fe_str} | Grade RE: {re_str} | Status: {status}")
if __name__ == "__main__":
    r= Result("SE21001", "IA2101", "PFP191", "Fall2026", 3, 3.0)
    r.display_result()