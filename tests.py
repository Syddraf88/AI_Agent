from functions.get_file_content import get_file_content

#result = get_file_content("calculator", "lorem.txt")

#print(result)

test1_result = get_file_content("calculator", "main.py")

test2_result = get_file_content("calculator", "pkg/calculator.py")

test3_result = get_file_content("calculator", "/bin/cat")

test4_result = get_file_content("calculator", "pkg/does_not_exit.py")

print(test1_result)

print(test2_result)

print(test3_result)

print(test4_result)