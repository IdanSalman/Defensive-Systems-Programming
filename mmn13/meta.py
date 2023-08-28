import os

project_file = input("Enter python file name: ")

# os.path.abspath is to make sure the path is converted to a file path according to different os.
with open(os.path.abspath(os.getcwd() + "/mmn13/" + project_file), "r") as f:
    stringified_file = f.read()

updated_file_string = stringified_file
python_code = input("Enter a python code (Enter -1 to stop): ")
while python_code != "-1":
    updated_file_string = updated_file_string + python_code + "\n"
    print("Added Code!")
    python_code = input("Enter a python code: ")

exec(updated_file_string)
