import os


class DataBase:
    def __init__(self):
        self.filename = None
        self.courses = None

    def load(self, semester_number):
        self.filename = f"semester-{semester_number}.csv"
        self.courses = {}

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                pass
            return ""

        with open(self.filename, "r") as file:
            for i, line in enumerate(file, start=1):
                c_name, c_credits, c_type_of_type_of_comp, c_grade = line.strip().split(";")
                c_name, c_credits, c_type_of_type_of_comp, c_grade = c_name.strip(), c_credits.strip(), c_type_of_type_of_comp.strip(), c_grade.strip()
                error = check_data(c_name, c_credits, c_type_of_type_of_comp, c_grade)

                if error != "":
                    return f"Error: Wrong content in line {i} in {self.filename}\n{error}"
                self.courses[c_name] = (c_credits, c_type_of_type_of_comp, c_grade)
        return ""

    def save(self, courses):
        with open(self.filename, "w") as f:
            for course in courses:
                f.write(f"{course};{courses[course][0]};{courses[course][1]};{courses[course][2]}\n")


def check_data(c_name, c_credits, c_type_of_type_of_comp, c_grade):
    error = check_name(c_name)
    if error != "":
        return error

    error = check_credits(c_credits)
    if error != "":
        return error

    error = check_type_of_completion(c_type_of_type_of_comp)
    if error != "":
        return error

    error = check_grade(c_grade)
    if error != "":
        return error

    return ""


def check_name(c_name):
    if c_name == "":
        return "Error: Name of course is needed."
    return ""


def check_credits(c_credits):
    if not c_credits.isdigit():
        return "Error: Credits is number value"
    return ""


def check_type_of_completion(c_type_of_completion):
    if c_type_of_completion in ["k", "zk", "z"]:
        return ""
    return "Error: Type of completion is [z/k/zk]."


def check_grade(c_grade):
    success_grades = ["A", "B", "C", "D", "E"]
    failing_grades = ["F", "X", "-"]
    if c_grade == "" or not all([x in success_grades + failing_grades for x in c_grade]):
        return "Error: Grade contains [A/B/C/D/E/F]"

    if len(c_grade) > 1:
        if not set(c_grade[:-1]).issubset({"F", "-"}):
            return "Error: Grade format is not right"

    return ""
