[![Black](https://github.com/falconizmi/average-grade-calculator/actions/workflows/black.yml/badge.svg)](https://github.com/falconizmi/average-grade-calculator/actions/workflows/black.yml)
[![Mypy Type Checker](https://github.com/falconizmi/average-grade-calculator/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/falconizmi/average-grade-calculator/actions/workflows/mypy.yml)
[![isort](https://github.com/falconizmi/average-grade-calculator/actions/workflows/isort.yml/badge.svg?branch=main)](https://github.com/falconizmi/average-grade-calculator/actions/workflows/isort.yml)
# Average Grade Calculator

This is an app coded in Python using Kivy, which calculates the average grade for a single term at Masaryk University. The calculation is based on the developer's understanding of the grading system at Masaryk University and is not affiliated with Masaryk University.

https://github.com/falconizmi/average-grade-calculator

## Requirements

To run this application, you will need:

- Python 3.9
- Git (if you want to clone the repository)

## Installation

Clone the repository using the following command:

```commandline
git clone https://github.com/falconizmi/average-grade-calculator.git
```

or download zip file.

Navigate to the project directory:

```commandline
cd average-grade-calculator
```

Install the required dependencies:

```commandline
pip install pipenv
pipenv shell
pipenv install
```

If windows and not working, then run this:

```commandline
pipenv install kivy_deps.sdl2
```


## Usage

To run the application, execute the following command:

```commandline
python averageGradeCalculator.py
```

Once the application is running, you will be directed to the Main window, input a number of the term you want to calculate into the provided field.

![image](https://user-images.githubusercontent.com/110352032/235273801-301b6d89-0b0a-404c-8492-c39e6521cc9c.png)

Click on the "Enter to Calculator" button to direct to the Calculator window.

![image](https://user-images.githubusercontent.com/110352032/235272725-13498c81-d9fd-4d47-97c4-97b4aa053ce6.png)

Click on the "Add Course" button to add a course to the table after filling Course Name, Credits, Type of Completion, and Grade into the provided fields.

Click on the "Calculate Average" button to get your average grade for the term.

Click on the "Clear" button to clear all added courses.

Click on the "Remove Last" button to remove the last added courses.

Click on the "Back to Main" button to return to the Main window.

Click on the "Save" button to save your added courses in a database for next choosing the same term.

## Contributing

Contributions to this project are welcome. If you encounter any issues, feel free to submit a bug report or pull request.

## License

This project is licensed under the MIT License.
