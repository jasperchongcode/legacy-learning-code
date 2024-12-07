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

def shift_list(key, message_list, type="encode"):
  shift_list = []
  if type == "encode":
   for idx in message_list:
    try:
     idx += next(key_iter)
    except:
     key_iter = iter(key)
     idx += next(key_iter)
    if idx >= 26:
     idx -= 26
    shift_list.append(idx)
  elif type == "decode":
   for idx in message_list:
    try:
     idx -= next(key_iter)
    except:
     key_iter = iter(key)
     idx -= next(key_iter)
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

while True:
  type = input("Encode or Decode? (e/d): ").lower()
  if type == "e":
    # get keyword
    keyword = input("Keyword: ").lower()
    # convert to integer
    key = message_to_int_list(keyword)
    print(key)

    # get message to encode
    message = input("Message: ").lower()
    # convert to integer
    message_list = message_to_int_list(message)
    print(message_list)

    # shift the message by the key
    shift_lst = shift_list(key, message_list)
    print(shift_lst)

    # turn the shifted message into letters
    final_message = int_list_to_message(shift_lst)

    # turn into a string
    msg = ""
    for letter in final_message:
      msg += letter
    print(msg)
  else:
    keyword = input("Keyword: ").lower()
    # convert to integer
    key = message_to_int_list(keyword)
    print(key)

    # get message to encode
    message = input("Message: ").lower()
    # convert to integer
    message_list = message_to_int_list(message)
    print(message_list)

    # shift the message by the key
    shift_lst = shift_list(key, message_list, type="decode")
    print(shift_lst)

    # turn the shifted message into letters
    final_message = int_list_to_message(shift_lst)

    # turn into a string
    msg = ""
    for letter in final_message:
      msg += letter
    print(msg)
 