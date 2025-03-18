"""A"""
from equations.Equation_solver import parse_equation
from Parser import tokenize, parse

def execute(type, tokens, start_value):
    match(type):
        case "FUNC_DEF":
            print(f"Defining a function with tokens : \n{tokens}")
        case "ASSIGNMENT":
            print(f"Defining a variable with tokens : \n{tokens}")
        case "EQUATION":
            print(f"Resolving an equation with tokens : \n{tokens}")
            parse_equation(start_value)
        case "EXPRESSION":
            print(f"Doing basic maths : \n{tokens}")
        case _:
            print(f"Unknown value : {type}. Tokens :\n{tokens}")

if __name__ == "__main__":
    while True:
        try:
            val = input("==> : ").strip().replace(" ", '')
            if val == "":
                continue
            tokens = tokenize(val)
            parsed = parse(tokens)
            execute(parsed["type"], parsed["tokens"], val)
        except EOFError:
            print("\nExiting ...")
            break
        except KeyboardInterrupt:
            print("\nExiting ...")
            break
        except ValueError as e:
            print(e)