from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from database import SessionDep, create_db_and_tables
from rds_model import Course
from models import CourseCreatePayload, UpdateCoursePayload
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # What to do before starting
    print("Server Starting...")
    create_db_and_tables()
    yield
    # What to do on stopping
    print("Server Stopping...")


server = FastAPI(
 title="Student Management API",
 lifespan=lifespan
)


@server.get("/") # Register a GET method for / route
def root():
    return {"message": "Go to /docs to see the API documentation"}

@server.get("/courses")
def list_all_courses(session: SessionDep):
    return session.scalars(select(Course)).all()

@server.get("/courses/{course_id}")
def get_course_by_id(course_id: int, session: SessionDep):
    course = session.get(Course, course_id) #pk matching
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return {"data": course}

@server.post("/courses", status_code=201)
def create_new_course(payload: CourseCreatePayload, session: SessionDep):
    new_course = Course(
        course_name=payload.course_name,
        course_difficulty=payload.course_difficulty,
    )

    session.add(new_course)
    session.commit()
    session.refresh(new_course)

    return {"data": new_course, "message": "New course created"}


@server.patch("/courses/{id}")
def update_course(id: int, payload: UpdateCoursePayload, session: SessionDep):
    course = session.get(Course, id)
    if not course:
        return {"message": "No course found with the given id"}

    if payload.course_name:
        course.course_name = payload.course_name
    if payload.course_difficulty:
        course.course_difficulty = payload.course_difficulty

    session.commit()
    session.refresh(course)

    return {"message": "Course Updated", "data": course}

@server.delete("/courses/{id}")
def delete_course(id: int, session: SessionDep):
    course = session.get(Course, id)
    if not course:
        return {"message": "Course not found"}

    session.delete(course)
    session.commit()

    return {"message": "Course removed"}