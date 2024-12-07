def add(*args):
    sum = 0
    for n in args:
        sum += n
    return sum

print(add(5,6,10))

def calculate(n, **kwargs):
    n += kwargs['add']
    n *= kwargs['multiply']
    print(n)



calculate(2, add=3, multiply=5)

class car:
    def __init__(self, **kw):
        self.make = kw['make']
        self.model = kw['model']
        
my_car = car(make='nissan', model = 'GT-R')