from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import database

from typing import Dict, Tuple


class MainWindow(Screen):
    semester_number = ObjectProperty(None)

    def enter_to_calculator(self) -> None:
        if not self.semester_number.text.isdigit():
            invalid_input_window("Number is needed.")
            return

        error = db.load(self.semester_number.text)
        if error != "":
            error_window(error)
            return

        sm.current = "calculator"
        self.semester_number.text = ""


class CalculatorWindow(Screen):
    course_name = ObjectProperty(None)
    course_credits = ObjectProperty(None)
    course_type_of_completion = ObjectProperty(None)
    course_grade = ObjectProperty(None)
    rv = ObjectProperty(None)

    def on_enter(self, *args: object) -> None:
        self.load()

    def back_to_main(self) -> None:
        self.clear_all()
        sm.current = "main"

    def add_course(self) -> None:
        # check if valid input
        error = database.check_data(
            self.course_name.text.strip(),
            self.course_credits.text.strip(),
            self.course_type_of_completion.text.strip(),
            self.course_grade.text.strip(),
        )
        if error != "":
            invalid_input_window(error)
            return

        self.rv.data.insert(
            0,
            {
                "name.text": self.course_name.text.strip(),
                "credits.text": self.course_credits.text.strip(),
                "type_of_completion.text": self.course_type_of_completion.text.strip(),
                "grade.text": self.course_grade.text.strip(),
            },
        )

        self.course_name.text = ""
        self.course_credits.text = ""
        self.course_type_of_completion.text = ""
        self.course_grade.text = ""

    def save(self) -> None:
        courses: Dict[str, Tuple[str, str, str]] = {}
        for row in self.rv.data:
            courses[row["name.text"]] = (
                row["credits.text"],
                row["type_of_completion.text"],
                row["grade.text"],
            )
        db.save(courses)

    def load(self) -> None:
        assert db.courses is not None
        for c_name, rest in db.courses.items():
            self.rv.data.insert(
                0,
                {
                    "name.text": c_name,
                    "credits.text": rest[0],
                    "type_of_completion.text": rest[1],
                    "grade.text": rest[2],
                },
            )

    def clear_all(self) -> None:
        self.rv.data = []

    def remove_last(self) -> None:
        if self.rv.data:
            self.rv.data.pop(0)
        else:
            invalid_input_window("There is no data")

    def calculate_average(self) -> None:
        if not self.rv.data:
            error_window("No grades to calculate average")
            return

        grade_value = {
            "A": 1,
            "B": 1.5,
            "C": 2,
            "D": 2.5,
            "E": 3,
            "F": 4,
            "X": 4,
            "-": 4,
        }
        sum_grade_credits = 0.0
        sum_credits = 0
        for row in self.rv.data:
            if row["type_of_completion.text"] != "zk":
                continue

            for grade in row["grade.text"]:
                credits_g = int(row["credits.text"])
                sum_grade_credits += grade_value[grade] * credits_g
                sum_credits += credits_g

        calculated_grade_window(round(sum_grade_credits / sum_credits, 2))


class WindowManager(ScreenManager):
    pass


def error_window(error: str) -> None:
    content = GridLayout(cols=1)
    content.add_widget(Label(text=error))
    content.add_widget(
        Label(text="(To close this window click anywhere outside the window.)")
    )
    pop = Popup(title="Error", content=content, size_hint=(None, None), size=(400, 400))
    pop.open()


def invalid_input_window(error: str) -> None:
    content = GridLayout(cols=1)
    content.add_widget(Label(text=error))
    content.add_widget(
        Label(text="(To close this window click anywhere outside the window.)")
    )
    pop = Popup(
        title="Invalid Input", content=content, size_hint=(None, None), size=(400, 400)
    )
    pop.open()


def calculated_grade_window(average: float) -> None:
    pop = Popup(
        title="Calculated Grade",
        content=Label(text=f"Calculated grade: {average}"),
        size_hint=(None, None),
        size=(400, 400),
    )

    pop.open()


kv = Builder.load_file("calculatorVisualisation.kv")

db = database.DataBase()

sm = WindowManager()

screens = [MainWindow(name="main"), CalculatorWindow(name="calculator")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"


class AverageGradeCalculatorApp(App):
    def build(self) -> WindowManager:
        return sm


if __name__ == "__main__":
    AverageGradeCalculatorApp().run()
