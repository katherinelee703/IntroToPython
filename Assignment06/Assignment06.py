# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions,
# classes, files, and exception handling while following
# the Separation of Concerns (SoC) pattern.
# Change Log: (Who, When, What)
#   KLee, 3/4/2026, Updated code to use classes & functions
# ------------------------------------------------------------------------------------------ #

import json
import _io

# -- Define the Data Constants -- #
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

menu_choice: str = ""
students: list = []
file = _io.TextIOWrapper


# -- Processing -- #
class FileProcessor:
    """
    A group of processing layer functions that work with JSON files
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Read JSON data from a file into a list of dictionary rows

        :param file_name: str data of the file's name
        :param student_data: list data to load from file contents
        :return: list of dictionary rows
        """
        global file
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
        except FileNotFoundError as e:
            IO.output_error_messages(
                "Error: The data file was not found. Starting with an empty list.",
                e
            )
            student_data = []
        except json.JSONDecodeError as e:
            IO.output_error_messages(
                "Error: The data file is not valid JSON. Starting with an empty list.",
                e
            )
            student_data = []
        except Exception as e:
            IO.output_error_messages(
                "Error: There was a non-specific problem reading the file.",
                e
            )
            student_data = []
        finally:
            try:
                if file and (file.closed is False):
                    file.close()
            except Exception:
                pass
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        Write JSON data from a list of dictionary rows to a file

        :param file_name: str data with the file name
        :param student_data: list data to write to the file
        :return: None
        """
        global file
        try:
            file = open(file_name, "w")
            json.dump(student_data, file, indent=2)
        except TypeError as e:
            IO.output_error_messages(
                "Error: The data could not be written as JSON. Please check the data types.",
                e
            )
        except Exception as e:
            IO.output_error_messages(
                "Error: There was a problem writing to the file. Is it open somewhere else?",
                e
            )
        finally:
            try:
                if file and (file.closed is False):
                    file.close()
            except Exception:
                pass


# -- Presentation -- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output.
    """
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Display a custom error message (and optional technical details)

        :param message: str description of what went wrong (friendly)
        :param error: optional technical Exception error info
        :return: None
        """
        print(message)
        if error is not None:
            print("-- Technical Error Message --")
            print(error.__doc__)
            print(str(error))
        print()

    @staticmethod
    def output_menu(menu: str):
        """ Display the menu """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """ Get the user's menu choice """
        return input("What would you like to do: ").strip()

    @staticmethod
    def output_student_courses(student_data: list):
        """ Display student registrations as comma-separated values """
        if len(student_data) == 0:
            print("No registrations have been entered yet.")
            print()
            return

        print("-" * 50)
        for row in student_data:
            try:
                print(f'{row["FirstName"]},{row["LastName"]},{row["CourseName"]}')
            except Exception as e:
                IO.output_error_messages("Error: Could not display a row of data.", e)
        print("-" * 50)
        print()

    @staticmethod
    def input_student_data(student_data: list):
        """
        Collect and validate one registration row from the user

        :param student_data: list with registration data
        :return: list with registration data
        """
        try:
            first_name = input("Enter the student's first name: ").strip()
            if not first_name.isalpha():
                raise ValueError("The first name should only contain letters.")
        except Exception as e:
            IO.output_error_messages("Error: Invalid first name.", e)
            return None

        try:
            last_name = input("Enter the student's last name: ").strip()
            if not last_name.isalpha():
                raise ValueError("The last name should only contain letters.")
        except Exception as e:
            IO.output_error_messages("Error: Invalid last name.", e)
            return None

        try:
            course = input("Please enter the name of the course: ").strip()
            if course == "":
                raise ValueError("The course name should not be empty.")
            return {"FirstName": first_name,
                    "LastName": last_name,
                    "CourseName": course}
        except Exception as e:
            IO.output_error_messages("Error: Invalid course.", e)
            return None


# -- Main Body -- #
students = FileProcessor.read_data_from_file(FILE_NAME, students)

while True:
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()
    print()

    if menu_choice == "1":
        new_row = IO.input_student_data(students)
        if new_row is not None:
            students.append(new_row)
            print(f'You have registered {new_row["FirstName"]} '
                  f'{new_row["LastName"]} for {new_row["CourseName"]}.')
            print()
        continue

    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)
        print("The following data was saved to file!")
        IO.output_student_courses(students)
        continue

    elif menu_choice == "4":
        break

    else:
        print("Please only choose option 1, 2, 3, or 4.\n")

print("Program Ended")

