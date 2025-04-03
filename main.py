"""A"""
from equations.Equation_solver import parse_equation
from Parser import tokenize, parse

from maths.Complex import Complex
from maths.Operations import calculate

from config import store, retrieve, display

def execute(type, tokens, start_value):
    match(type):
        case "FUNC_DEF":
            print(f"Defining a function with tokens : \n{tokens}")
        case "VARIABLE_DISPLAY":
            value = retrieve(tokens[0][1])
            if value is None:
                print("No such variable.")
            else:
                print(value)
        case "ASSIGNMENT":
            store(tokens[2][1], tokens[0][1])
        case "EQUATION":
            parse_equation(start_value)
        case "EXPRESSION":
            if tokens[1] == '?':
                display()
            else:
                calculate(tokens)
        case _:
            print(f"Unknown value : {type}. Tokens :\n{tokens}")

if __name__ == "__main__":
    while True:
        try:
            val = input("==> : ")
            if val.strip().replace(" ", '') == "":
                continue
            try:
                tokens = tokenize(val)
                parsed = parse(tokens)
                execute(parsed["type"], parsed["tokens"], val)
            except SyntaxError as e:
                print(f"Error - Invalid syntax : {e}")
        except EOFError:
            print("\nExiting ...")
            break
        except KeyboardInterrupt:
            print("\nExiting ...")
            break
        except ValueError as e:
            print(e)