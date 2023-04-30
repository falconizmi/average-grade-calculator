import os
from typing import Dict, Optional, Tuple


class DataBase:
    def __init__(self) -> None:
        self.filename: Optional[str] = None
        self.courses: Optional[Dict[str, Tuple[str, str, str]]] = None

    def load(self, semester_number: str) -> str:
        self.filename = f"semester-{semester_number}.csv"
        self.courses = {}

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                pass
            return ""

        with open(self.filename, "r") as file:
            for i, line in enumerate(file, start=1):
                c_name, c_credits, c_type_of_type_of_comp, c_grade = line.strip().split(
                    ";"
                )
                c_name, c_credits, c_type_of_type_of_comp, c_grade = (
                    c_name.strip(),
                    c_credits.strip(),
                    c_type_of_type_of_comp.strip(),
                    c_grade.strip(),
                )
                error = check_data(c_name, c_credits, c_type_of_type_of_comp, c_grade)

                if error != "":
                    return (
                        f"Error: Wrong content in line {i} in {self.filename}\n{error}"
                    )
                self.courses[c_name] = (c_credits, c_type_of_type_of_comp, c_grade)
        return ""

    def save(self, courses: Dict[str, Tuple[str, str, str]]) -> None:
        assert self.filename is not None
        with open(self.filename, "w") as f:
            for course in courses:
                f.write(
                    f"{course};{courses[course][0]};{courses[course][1]};{courses[course][2]}\n"
                )


def check_data(
    c_name: str, c_credits: str, c_type_of_type_of_comp: str, c_grade: str
) -> str:
    error = check_name(c_name)
    if error != "":
        return error

    error = check_credits(c_credits)
    if error != "":
        return error

    error = check_type_of_completion(c_type_of_type_of_comp)
    if error != "":
        return error

    error = check_grade(c_grade, c_type_of_type_of_comp)
    if error != "":
        return error

    return ""


def check_name(c_name: str) -> str:
    if c_name == "":
        return "Error: Name of course is needed."
    return ""


def check_credits(c_credits: str) -> str:
    if not c_credits.isdigit():
        return "Error: Credits is number value"
    return ""


def check_type_of_completion(c_type_of_completion: str) -> str:
    if c_type_of_completion in ["k", "zk", "z"]:
        return ""
    return "Error: Type of completion is [z/k/zk]."


def check_grade(c_grade: str, c_type_of_completion: str) -> str:
    zk_success_grades = ["A", "B", "C", "D", "E"]
    zk_fail_grades = ["F"]
    z_k_success_grades = ["P"]
    z_k_fail_grades = ["N"]
    other_fail_grades = ["X", "-"]
    if c_type_of_completion == "zk":
        if c_grade == "" or not all(
            [
                x in zk_success_grades + zk_fail_grades + other_fail_grades
                for x in c_grade
            ]
        ):
            return "Error: Grade contains [A/B/C/D/E/F/X/-]"
    else:
        if c_grade == "" or not all(
            [
                x in z_k_success_grades + z_k_fail_grades + other_fail_grades
                for x in c_grade
            ]
        ):
            return "Error: Grade contains [P/N/X/-]"

    if len(c_grade) > 1:
        if not (
            set(c_grade[:-1]).issubset({"F", "-"})
            or set(c_grade[:-1]).issubset({"N", "-"})
        ):
            return "Error: Grade format is not right"

    return ""
