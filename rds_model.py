from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# every SQLAlchemy model needs a parent class.
class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_name: Mapped[str]
    course_difficulty: Mapped[str]