from functions.get_files_info import get_files_info

tests = [["calculator", "."],
         ["calculator", "pkg"],
         ["calculator", "/bin"],
         ["calculator", "../"]
         ]


def run_test(tests):
    for test in tests:
        result = get_files_info(test[0], test[1])
        print(result)

def main():
    run_test(tests)

main()