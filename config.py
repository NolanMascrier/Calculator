from maths.Complex import Complex


VARIABLES = [["test", Complex(42, 0)]]
FUNCTIONS = []

def store(value, name):
    global VARIABLES
    VARIABLES.append([name, value])

def display():
    print("### Stored Variables :")
    for data in VARIABLES:
        print(data[0], "=", data[1])
    print("### Stored Functions :")
    for data in FUNCTIONS:
        print(data)

def retrieve(key):
    for data in VARIABLES:
        if data[0] == key:
            return data[1]
    return None