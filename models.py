from pydantic import BaseModel


class CourseCreatePayload(BaseModel):
    course_name: str
    course_difficulty: str


class UpdateCoursePayload(BaseModel):
    course_name: str | None = None
    course_difficulty: str | None = None


class StudentCreatePayload(BaseModel):
    student_id : int 
    name : str 
    age : int | None=None
    address : str | None=None
    email : str | None=None
    phone : str | None=None


class UpdateStudentPayload(BaseModel):
    name : str |None=None
    age : int | None=None
    address : str | None=None
    email : str | None=None
    phone : str | None=None