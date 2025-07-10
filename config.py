"""File containing containing the Function/Variable storages and the methods \
    to access them."""

VARIABLES = []
FUNCTIONS = []

def store(value, name, isFunction = False):
    """Stores a function or a variable.
    
    Args:
        value (Node): value to save as an Abstract Syntax Tree.
        name (str): name of the the value to store.
        isFunction(bool, optionnal) : if set to `True`, the value \
        will be saved as a function rather than a variable. Defaults \
        to `False`.
    
    Raises:
        SyntaxError : The variable/function has a forbidden name (x)
    """
    global VARIABLES
    flag = False
    if name.lower() == 'x':
        raise SyntaxError(f"Cannot use {name} as a variable name !")
    if isFunction:
        for data in FUNCTIONS:
            if data[0] == name:
                flag = True
                data[1] = value
        if flag is False:
            FUNCTIONS.append([name, value])
    else:
        for data in VARIABLES:
            if data[0] == name:
                flag = True
                data[1] = value
        if flag is False:
            VARIABLES.append([name, value])

def display():
    """Displays the stored variable and functions.
    """
    print("### Stored Variables :")
    for data in VARIABLES:
        print(f"{str(data[0])} = {str(data[1])}")
    print("### Stored Functions :")
    for data in FUNCTIONS:
        print(f"{str(data[0])}(x) = {str(data[1])}")

def retrieve(key, isFunction = False):
    """Retrieve and solve a function or a variable.
    
    Args:
        key (str): Name of the searched function or variable.
        isFunction (bool, optionnal) : if set to `True`, will \
        attempt to search for a function rather than a variable. \
        Defaults to False.
    
    Raises:
        IndexError : Unknown key for VARIABLE or FUNCTIONS.      

    Returns:
        (Complex|Matrix) : Computed stored variable or \
        function.
    """
    if isFunction:
        index = key.find("(")
        if index != -1:
            key = key[:index]
        for data in FUNCTIONS:
            if data[0].lower() == key.lower():
                return data[1]
    else:
        for data in VARIABLES:
            if data[0].lower() == key.lower():
                return data[1]
    raise IndexError(key)