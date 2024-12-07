import hashlib

m = hashlib.sha256()


# b means bytes format
text = b"1"

m.update(text)

key = m.hexdigest()
print(key)

while True:
    if hashlib.sha256(str.encode(input("Input password: "))).hexdigest() == key:
        print("pass")
    else:
        print("fail")