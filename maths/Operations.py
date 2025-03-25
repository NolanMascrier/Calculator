"""Holds calculation functions."""

from maths.Complex import Complex
import config

def retrieve(key):
    for data in config.VARIABLES:
        if data["name"] == key:
            return data["value"]
    return None

def calculate(tokens):
    """Calculate the operation between left and
    right. All variable must be tokens.
    
    Args:
        right (tuple): right tokens of the operation.
        operator (tuple): operator of the operation.
        left (tuple): left tokens of the operation. 
    """
    print(f"Doing basic maths : \n{tokens}")
    pass