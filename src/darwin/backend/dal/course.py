from darwin.backend.dal.dal_I import Dal_I
from itertools import chain
from darwin.models.backend_models import (
    Account as M_Account,
    Student as M_Student,
    Teacher as M_Teacher,
    Course as M_Course,
    CourseId,
    AccountId,
)
from darwin.backend.schemas import (
    Course as S_Course,
    Account as S_Account,
    Student as S_Student,
    Ta as S_Ta,
    Teacher as S_Teacher,
)


class CourseDal(Dal_I):

    def create(self, course: M_Course):
        with self.db_session() as db:
            db_course: S_Course = S_Course(
                id=course.id, name=course.name, deleted=course.deleted
            )
            db.add(db_course)
            db.commit()

    def get_all(self, show_deleted=False) -> list[M_Course]:
        with self.db_session() as db:
            db_courses = db.query(S_Course)
            if not show_deleted:
                db_courses = db_courses.filter(S_Course.deleted == False)
            return [
                M_Course.model_validate(db_course) for db_course in db_courses.all()
            ]

    def get(self, id: CourseId, show_deleted=False) -> M_Course:
        with self.db_session() as db:
            if show_deleted:
                db_course = db.query(S_Course).filter(S_Course.id == id).one()
            else:
                db_course = (
                    db.query(S_Course)
                    .filter(S_Course.id == id and S_Course.deleted == False)
                    .one()
                )
            db.close()
            return M_Course.model_validate(db_course)

    # Get teachers from course
    def get_student_courses_by_account(self, account_id: AccountId) -> list[M_Course]:
        with self.db_session() as db:
            student_courses = (
                db.query(S_Course, S_Student)
                .join(S_Student, S_Course.id == S_Student.course_f)
                .where(S_Student.account_f==account_id)
                .all()
            )
            return [M_Course.model_validate(sc.Course) for sc in student_courses]
    

    def get_ta_courses_by_account(self, account_id: AccountId) -> list[M_Course]:
        with self.db_session() as db:
            ta_courses = (
                db.query(S_Course, S_Ta)
                .join(S_Ta, S_Course.id == S_Ta.course_f)
                .where(S_Ta.account_f==account_id)
                .all()
            )
            return [M_Course.model_validate(tc.Course) for tc in ta_courses]


    def get_teacher_courses_by_account(self, account_id: AccountId) -> list[M_Course]:
        with self.db_session() as db:
            teacher_courses = (
                db.query(S_Course, S_Teacher)
                .join(S_Teacher, S_Course.id == S_Teacher.course_f)
                .where(S_Teacher.account_f==account_id)
                .all()
            )
            return [M_Course.model_validate(tc.Course) for tc in teacher_courses]




if __name__ == "__main__":
    from darwin.backend.db_init import SessionLocal

    course_dal = CourseDal(SessionLocal)
    ta_account = AccountId('dbbd561d-c82f-4fbc-88f2-f44a3907b695')
    student_account = AccountId('b0898155-f44f-448c-8b41-e2f82480f380')
    course_dal.get_courses_by_account(
        student_account
    )
