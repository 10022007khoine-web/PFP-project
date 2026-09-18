from Result import Result #Import Result class
#from File_Hanlder import FileHandler, FileIOException
class ResultManager:
    def __init__(self):
        #Khởi tạo danh sách kết quả 
        self._result: list[Result]= []
    def add_result(self, new_result: Result):
        """
        ======1. Add a new result to system======
        """
        #Check if student_id and course_id already exists
        for r in self._result:
            if r.student_id == new_result.student_id and r.course_id == new_result.course_id:
                print(f"Result already exists for Student ID: {new_result.student_id} in Course ID:{new_result.course_id} ")
            #End if 
        #End for 
        self._result.append(new_result)
        print("Updated successfully")
    #End def
    def update_result(self, student_id:str, course_id:str, grade_fe: float=None,grade_re: float=None)->bool:
        """
        ======2. Update FE or RE grade for a Student======
        """
        for r in self._result:
            if r.student_id == student_id and r.course_id == course_id:
                if grade_fe is not None:
                    r.grade_fe = grade_fe
                if grade_re is not None:
                    r.grade_re = grade_re
                return True 
            #End if 
        #End for 
        return False
    #End def 
    def search_student_id(self, student_id: str)->list[Result]:
        """
        ======3. Search/Display enrollment by Student ID======
        """
        found_result = []
        for r in self._result:
            if r.student_id == student_id:
                found_result.append(r)
        return found_result
    def get_sorted_by_status(self)->list[Result]:
        