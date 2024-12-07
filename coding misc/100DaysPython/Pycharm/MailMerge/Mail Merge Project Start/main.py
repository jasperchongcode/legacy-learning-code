#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

list = []
name_list = []
letter_template = ""
with open("Input/Names/invited_names.txt", 'r') as names:
    list = names.readlines()

for name in list:
    name = name.replace('\n', '')
    name_list.append(name)

with open("Input/Letters/starting_letter.txt", 'r') as letter:
    letter_template = letter.read()

for name in name_list:

    with open(f"Output/ReadyToSend/letter_for_{name}.txt",'w') as custom_letter:
        letter = letter_template.replace("[name]", f"{name}")
        custom_letter.write(letter)

