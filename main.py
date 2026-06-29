from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from database import SessionDep, create_db_and_tables
from rds_model import Course , Student
from models import CourseCreatePayload, UpdateCoursePayload , StudentCreatePayload , UpdateStudentPayload
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

### COURSES ###
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
    session.refresh(new_course)     # gives updated db with auto incremneted id

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


### STUDENTS ###

@server.get("/students")
def get_all_students(session:SessionDep):
    return session.scalars(select(Student)).all()

@server.get("/students/{student_id}")
def get_student_byid(id : int , session : SessionDep):
    student=session.get(Student,id)
    if not student:
        raise HTTPException(status_code=404 , detail="Student not found")
    return {"data":student}


@server.post("/students", status_code=201)
def create_new_student(payload: StudentCreatePayload, session: SessionDep):
    
    new_student = Student(
        student_id = payload.student_id,
        name = payload.name,
        age = payload.age,
        address = payload.address,
        email =payload.email,
        phone = payload.phone
    )

    session.add(new_student)
    session.commit()
    session.refresh(new_student)     # gives updated db with auto incremneted id

    return {"data": new_student, "message": "New student created"}


@server.patch("/students/{student_id}")
def update_student(student_id: int, payload: UpdateStudentPayload, session: SessionDep):
    student = session.get(Student, student_id)
    if not student:
        return {"message": "No student found with the given id"}

    if payload.name:
        student.name = payload.name
    if payload.age:
        student.age = payload.age
    if payload.address:
        student.address = payload.address
    if payload.email:
        student.email = payload.email
    if payload.phone:
        student.phone = payload.phone

    session.commit()
    session.refresh(student)

    return {"message": "Student Updated", "data": student}

@server.delete("/student/{student_id}")
def delete_course(student_id: int, session: SessionDep):
    student = session.get(Student, student_id)
    if not student:
        return {"message": "Student not found"}

    session.delete(student)
    session.commit()

    return {"message": "Student removed"}

    

