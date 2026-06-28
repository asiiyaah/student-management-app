from pydantic import BaseModel


class CourseCreatePayload(BaseModel):
    course_name: str
    course_difficulty: str


class UpdateCoursePayload(BaseModel):
    course_name: str | None = None
    course_difficulty: str | None = None