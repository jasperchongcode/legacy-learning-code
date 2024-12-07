import readline

file1_list = []
file2_list = []


with open("file1.txt",'r') as file1:
    file1_unstripped = file1.readlines()
    for number in file1_unstripped:
        number = number.strip()
        file1_list.append(number)

with open("file2.txt",'r') as file2:
    file2_unstripped = file2.readlines()
    for number in file2_unstripped:
        number = number.strip()
        file2_list.append(number)


result = [number for number in file1_list if number in file2_list]

# Write your code above 👆

print(result)






