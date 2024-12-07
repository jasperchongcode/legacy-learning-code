shift = {"a":0,
         "b":1,
         "c":2,
         "d":3,
         "e":4,
         "f":5,
         "g":6,
         "h":7,
         "i":8,
         "j":9,
         "k":10,
         "l":11,
         "m":12,
         "n":13,
         "o":14,
         "p":15,
         "q":16,
         "r":17,
         "s":18,
         "t":19,
         "u":20,
         "v":21,
         "w":22,
         "x":23,
         "y":24,
         "z":25}

def message_to_int_list(message):
 message_list = []
 for letter in message:
  message_list.append(shift[letter])
 return message_list

def shift_list(key, message_list, type="e"):
  shift_list = []
  if type == "e":
   for idx in message_list:
    idx += key
    if idx >= 26:
     idx -= 26
    shift_list.append(idx)
  elif type == "d":
   for idx in message_list:
    idx -= key
    if idx < 0:
     idx += 26
    shift_list.append(idx)
  return shift_list

def int_list_to_message(shift_list):
 final_message = []
 # message to text
 for idx in shift_list:
  letter = ""
  for (key,value) in shift.items():
   if value == idx:
    letter = key
  final_message.append(letter)
 return final_message

type = input("Encode/decode (e/d): ").lower()

key = int(input("Shift by: "))
message = input("Message: ")
# convert to integer list
message_list = message_to_int_list(message)
print(message_list)
# shift by the key
shift_lst = shift_list(key, message_list, type=type)
print(shift_lst)

# turn back into string
final_message = int_list_to_message(shift_lst)
msg = ""
for letter in final_message:
    msg += letter
print(msg)

