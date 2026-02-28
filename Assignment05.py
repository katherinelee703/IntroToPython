# ------------------------------------------------------------------------------------------ #
# Title: Assignment05
# Desc: This assignment demonstrates using dictionaries, files, and exception handling
# Change Log: (Who, When, What)
#   KLee, 2/28/2026, Updated Script
# ------------------------------------------------------------------------------------------ #

# TODO: Import the json and _io modules
import json
import _io

# Define the Data Constants
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

# Define the Data Variables
student_first_name: str = ""
student_last_name: str = ""
course_name: str = ""
file = _io.TextIOWrapper  # Allows us to use file.close() in the finally block
menu_choice: str = ""
student_data: dict = {}   # one row of student data (dictionary)
students: list = []       # a table of student data (list of dictionaries)


# When the program starts, read the file data into a list of dictionaries (table)
try:
    file = open(FILE_NAME, "r")
    students = json.load(file)
except FileNotFoundError as e:
    print("Text file must exist before running this script!\n")
    print("-- Technical Error Message -- ")
    print(e, e.__doc__, type(e), sep="\n")
    students = []
except Exception as e:
    print("There was a non-specific error!\n")
    print("-- Technical Error Message -- ")
    print(e, e.__doc__, type(e), sep="\n")
    students = []
finally:
    try:
        file.close()
    except Exception:
        pass


# Present and process the data
while True:

    # Present the menu of choices
    print(MENU)
    menu_choice = input("What would you like to do: ")

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!

        # Structured error handling for first name input
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should only contain letters.")
        except ValueError as e:
            print(e)
            print("-- Technical Error Message -- ")
            print(e.__doc__)
            print(e.__str__())
            continue
        except Exception as e:
            print("There was a non-specific error!\n")
            print("-- Technical Error Message -- ")
            print(e, e.__doc__, type(e), sep="\n")
            continue

        # Structured error handling for last name input
        try:
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should only contain letters.")
        except ValueError as e:
            print(e)
            print("-- Technical Error Message -- ")
            print(e.__doc__)
            print(e.__str__())
            continue
        except Exception as e:
            print("There was a non-specific error!\n")
            print("-- Technical Error Message -- ")
            print(e, e.__doc__, type(e), sep="\n")
            continue

        course_name = input("Please enter the name of the course: ")

        # Add the new data to a dictionary, then add it to the table (list of dictionaries)
        student_data = {"FirstName": student_first_name,
                        "LastName": student_last_name,
                        "Course": course_name}
        students.append(student_data)

        print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        continue

    # Present the current data
    elif menu_choice == "2":

        # Process the data to create and display a custom message
        print("-" * 50)
        for student in students:
            print(f"Student {student['FirstName']} {student['LastName']} is enrolled in {student['Course']}")
        print("-" * 50)

        # Also show comma-separated values for each row
        for student in students:
            print(f"{student['FirstName']},{student['LastName']},{student['Course']}")
        print("-" * 50)
        continue

    # Save the data to a file
    elif menu_choice == "3":

        # Structured error handling for writing dictionary rows to the file
        try:
            file = open(FILE_NAME, "w")
            json.dump(students, file)
            file.close()

            print("The following data was saved to file!")
            print("-" * 50)
            for student in students:
                print(f"Student {student['FirstName']} {student['LastName']} is enrolled in {student['Course']}")
            print("-" * 50)

        except Exception as e:
            print("-- Technical Error Message -- ")
            print("Built-In Python error info: ")
            print(e, e.__doc__, type(e), sep="\n")

        finally:
            try:
                file.close()
            except Exception:
                pass

        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

    else:
        print("Please only choose option 1, 2, 3, or 4.\n")
        continue

print("Program Ended")
