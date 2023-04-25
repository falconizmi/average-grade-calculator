from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup


class MainWindow(Screen):
    semester_digit = ObjectProperty(None)

    def enter_to_calculator(self):
        if not self.semester_digit.text.isdigit():
            invalid_input_window("Number is needed.")
        else:
            sm.current = "semester"
            self.semester_digit.text = ""


class SemesterWindow(Screen):
    course_name = ObjectProperty(None)
    course_credits = ObjectProperty(None)
    course_type_of_completion = ObjectProperty(None)
    course_grade = ObjectProperty(None)
    rv = ObjectProperty(None)

    def back_to_main(self):
        sm.current = "main"
        self.clear_all()

    def add_course(self):
        # check if valid input
        if not self.course_name.text != "":
            invalid_input_window("Error: Name of course is needed.")
            return

        if not self.course_credits.text.isdigit():
            invalid_input_window("Error: Credits is number value")
            return

        if not check_type_of_completion(self.course_type_of_completion.text):
            invalid_input_window("Error: Type of completion is [z/k/zk].")
            return

        grade_error = check_grade(self.course_grade.text)
        if grade_error != "":
            invalid_input_window(grade_error)
            return

        self.rv.data.insert(0, {"name.text": self.course_name.text,
                                "credits.text": self.course_credits.text,
                                "type_of_completion.text": self.course_type_of_completion.text,
                                "grade.text": self.course_grade.text
                                })

        self.course_name.text = ""
        self.course_credits.text = ""
        self.course_type_of_completion.text = ""
        self.course_grade.text = ""

    def clear_all(self):
        self.rv.data = []

    def remove_last(self):
        if self.rv.data:
            self.rv.data.pop(0)
        else:
            invalid_input_window("There is no data")

    def calculate_average(self):
        if not self.rv.data:
            error_window("No grades to calculate average")
            return 

        grade_value = {"A": 1, "B": 1.5,
                       "C": 2, "D": 2.5,
                       "E": 3, "F": 4,
                       "X": 4, "-": 4}
        sum_grade_credits = 0
        sum_credits = 0
        for row in self.rv.data:
            for grade in row["grade.text"]:
                credits_g = int(row["credits.text"])
                sum_grade_credits += grade_value[grade] * credits_g
                sum_credits += credits_g

        calculated_grade_window(round(sum_grade_credits/sum_credits, 2))



class WindowManager(ScreenManager):
    pass


def error_window(error):
    content = GridLayout(cols=1)
    content.add_widget(Label(text=error))
    content.add_widget(Label(text="(To close this window click anywhere outside the window.)"))
    pop = Popup(title='Error',
                content=content,
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalid_input_window(error):
    content = GridLayout(cols=1)
    content.add_widget(Label(text=error))
    content.add_widget(Label(text="(To close this window click anywhere outside the window.)"))
    pop = Popup(title='Invalid Input',
                content=content,
                size_hint=(None, None), size=(400, 400))
    pop.open()


def calculated_grade_window(average):
    pop = Popup(title='Calculated Grade',
                content=Label(text=f'Calculated grade: {average}'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


def check_type_of_completion(type_of_completion):
    return type_of_completion in ["k", "zk", "z"]


def check_grade(grade):
    success_grades = ["A", "B", "C", "D", "E"]
    failing_grades = ["F", "X", "-"]
    if grade == "" or not all([x in success_grades + failing_grades for x in grade]):
        return "Error: Grade contains [A/B/C/D/E/F]"

    if len(grade) > 1:
        if not set(grade[:-1]).issubset({"F", "-"}):
            return "Error: Grade format is not right"

    return ""


kv = Builder.load_file("calculatorVisualisation.kv")

sm = WindowManager()

screens = [MainWindow(name="main"), SemesterWindow(name="semester")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"


class AverageGradeCalculatorApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    AverageGradeCalculatorApp().run()
