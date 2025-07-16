from functions import get_files_info
from functions.get_file_content import get_file_content

tests = [["calculator", "main.py"],
         ["calculator", "pkg/calculator.py"],
         ["calculator", "/bin/cat"],
         ["calculator", "pkg/doesn_not_exist.py"]
         ]


def run_test(tests):
    for test in tests:
        result = get_file_content(test[0], test[1])
        print(result)

def main():
    run_test(tests)

main()