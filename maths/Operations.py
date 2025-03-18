"""Holds calculation functions."""

def plus(right, left):
    """A + between left and right."""
    return left[1] + right[1]

def calculate(right, operator, left):
    """Calculate the operation between left and
    right. All variable must be tokens.
    
    Args:
        right (tuple): right tokens of the operation.
        operator (tuple): operator of the operation.
        left (tuple): left tokens of the operation. 
    """
    if not operator or operator[0] != "OP":
        return
    match (operator[1]):
        case "+":
            result = plus(right, left)
        case "-":
            pass
        case "/":
            pass
        case "*":
            pass
        case "%":
            pass
        case "**":
            pass
        case "^":
            pass
        case _:
            return
    print(result)