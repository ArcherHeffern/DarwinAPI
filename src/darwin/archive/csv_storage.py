from typing import Self
from models.backend_models import Assignment, Student, TestResult
from csv import DictWriter
from pathlib import Path


class CSVStorage:
    def __init__(self, assignment: Assignment, file: Path):
        self.assignment = assignment
        self.file = file
        self.writer = None
        self.f = None

    def __enter__(self) -> Self:
        self.f = open(self.file, "w")
        self.writer = DictWriter(
            self.f, ("student", "passing", "failing", "erroring", "skipped")
        )
        self.writer.writeheader()
        return self

    def __exit__(self, *args):
        if self.f:
            self.f.close()

    def upload_grade(self, student: Student, test_result: TestResult):
        if self.writer:
            self.writer.writerow(
                {
                    "student": student.name,
                    "passing": len(test_result.passing_tests),
                    "erroring": len(test_result.erroring_tests),
                    "failing": len(test_result.failing_tests),
                }
            )
        if self.f:
            self.f.flush()

    def upload_grades(self, students: list[Student]):
        raise NotImplementedError

    def load_grade(self, student: Student):
        raise NotImplementedError

    def load_grades(self, student: Student):
        raise NotImplementedError
