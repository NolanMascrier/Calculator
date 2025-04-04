from maths.Complex import Complex


VARIABLES = []
FUNCTIONS = []

def store(value, name, isFunction = False):
    global VARIABLES
    if name.lower() == 'x' or name.lower() == 'i':
        raise ValueError(f"Cannot use {name} as a variable name !")
    if isFunction:
        FUNCTIONS.append([name, value])
    else:
        VARIABLES.append([name, value])

def display():
    print("### Stored Variables :")
    for data in VARIABLES:
        print(f"{str(data[0])} = {str(data[1])}")
    print("### Stored Functions :")
    for data in FUNCTIONS:
        print(f"{str(data[0])}(x) = {str(data[1])}")

def retrieve(key, isFunction = False, x = None):
    if isFunction:
        for data in FUNCTIONS:
            if data[0].lower() == key.lower():
                return data[1].solve(x)
    else:
        for data in VARIABLES:
            if data[0].lower() == key.lower():
                return data[1].solve()
    return None