# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes,
#       inheritance, and 
# Change Log: (Who, When, What)
#   KLee, 3/11/2026, Updated Script
# ------------------------------------------------------------------------------------------ #
import json
import _io

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str = ""  # Hold the choice made by the user.


class Person:
    """A class representing person data with validated name properties."""

    def __init__(self, first_name: str = "", last_name: str = ""):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self):
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self):
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """A class representing student registration data."""

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name.title()

    @course_name.setter
    def course_name(self, value: str):
        if isinstance(value, str):
            self.__course_name = value
        else:
            raise ValueError("The course name should be a string.")

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.course_name}"


# Processing --------------------------------------- #
class FileProcessor:
    """A collection of processing layer functions that work with JSON files."""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Read JSON data from a file and convert dictionary rows into Student objects."""
        file = _io.TextIOWrapper

        try:
            file = open(file_name, "r")
            json_students = json.load(file)

            for student in json_students:
                student_object = Student(first_name=student["FirstName"],
                                         last_name=student["LastName"],
                                         course_name=student["CourseName"])
                student_data.append(student_object)

            file.close()

        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            try:
                if file.closed == False:
                    file.close()
            except Exception:
                pass

        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Write Student objects to a JSON file by converting them to dictionary rows."""
        file = _io.TextIOWrapper

        try:
            json_students: list = []
            for student in student_data:
                student_dict = {"FirstName": student.first_name,
                                 "LastName": student.last_name,
                                 "CourseName": student.course_name}
                json_students.append(student_dict)

            file = open(file_name, "w")
            json.dump(json_students, file, indent=2)
            file.close()
            IO.output_student_courses(student_data=student_data)

        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            try:
                if file.closed == False:
                    file.close()
            except Exception:
                pass


# Presentation --------------------------------------- #
class IO:
    """A collection of presentation layer functions that manage user input and output."""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Display a custom error message to the user."""
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """Display the menu of choices to the user."""
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        """Get a menu choice from the user."""
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """Display the student and course names as comma-separated values."""
        print("-" * 50)
        for student in student_data:
            print(str(student))
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """Get the student's first name, last name, and course name from the user."""
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the name of the course: ")

            student = Student(first_name=student_first_name,
                              last_name=student_last_name,
                              course_name=course_name)

            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was not the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

while True:

    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":
        break
    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")
