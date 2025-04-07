"""A"""
from equations.Equation_solver import parse_equation
from Parser import tokenize, parse

from maths.Complex import Complex

from config import store, retrieve, display

from syntax_tree import build_ast

def execute(type, tokens, start_value):
    """Executes the command. 
    
    Args:
        type (string): Type of the command. Can be FUNC_DEF, VARIABLE_DISPlAY, \
        ASSIGNMENT, EQUATION or EXPRESSION.
        tokens (list|tuple): list of tokens to use. Can also be a single tuple \
        in some cases. 
        start_value (str): backup of the original input. Only used for equation \
        solving.
    """
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
            print(tokens)
            name = tokens[0][1]
            tokens.pop(0)
            tokens.pop(0)
            print(tokens)
            ast = build_ast(tokens)
            print(ast)
            store(ast, name)
        case "EQUATION":
            parse_equation(start_value)
        case "EXPRESSION":
            if tokens[1] == '?':
                display()
            else:
                ast = build_ast(tokens)
                result = ast.solve()
                print(result)
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
            except ValueError as e:
                print(f"Error - Invalid value : {e}")
            except AttributeError as e:
                print(f"Error - Unsupporte operation : {e}")
        except EOFError:
            print("\nExiting ...")
            break
        except KeyboardInterrupt:
            print("\nExiting ...")
            break
        except ValueError as e:
            print(e)