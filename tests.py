from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def test():
    result = get_file_content("calculator", "main.py")
    print("File content for calculator/main.py:")
    print(result)
    print("\n")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("File content for calculator/pkg/calculator.py:")
    print(result)
    print("\n")
    
    result = get_file_content("calculator", "/bin/cat")
    print("File content for calculator/bin/cat")
    print(result)
    print("\n")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("File content for calculator/pkg/does_not_exist.py")
    print(result)
    print("\n")
    
    # result = get_file_content("calculator", "lorem.txt")
    # print("Result for calculator, lorem:")
    # print(result)
    # print("\n")

test()

