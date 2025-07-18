from functions import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_files import run_python_files

tests = [["calculator", "main.py"],
         ["calculator", "main.py", ["3 + 5"]],
         ["calculator", "tests.py"],
         ["calculator", "../main.py"],
         ["calculator", "nonexistent.py"]
         ]


def run_test(tests):
    for test in tests:
        if len(test) > 2:
            result = run_python_files(test[0], test[1], test[2])
        else:
            result = run_python_files(test[0], test[1])
        print(result)

def main():
    run_test(tests)

main()