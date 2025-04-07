"""File for the execution process."""
from syntax_tree import build_ast
from config import store, retrieve, display

from maths.Complex import Complex
from equations.Equation_solver import parse_equation
from syntax_tree import Node

#Used ONLY for the curves
import matplotlib.pyplot as plt
import numpy as np

def token_strip(tokens):
    """Strips the tokens of the name and the = operator \
    for assignment purposes.

    Args:
        tokens (list) : Token list to strip.
    
    Returns:
        (list, str): Stripped token list and retrieved name.
    """
    name = tokens[0][1]
    index = name.find("(")
    if index != -1:
        name = name[:index]
    tokens.pop(0)
    tokens.pop(0)
    return tokens, name

def display_curve(tree, name):
    """Displays a curve with numpy and matplotlib.

    Args:
        tree (Node) : Abstract Syntax Tree containing the \
        function.
    """
    x_vals = np.linspace(-10, 10, 400)
    y_vals = []
    for x in x_vals:
        y = tree.solve(Complex(x)).real
        y_vals.append(y)

    plt.plot(x_vals, y_vals, label=str(tree))
    plt.xlabel('x')
    plt.ylabel(f'{name}(x)')
    plt.title('Plot from AST')
    plt.grid(True)
    plt.legend()
    plt.get_current_fig_manager().set_window_title(f'Plotting curve for {name}(x)')
    plt.show()

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
            tokens, name = token_strip(tokens)
            ast = build_ast(tokens)
            store(ast, name, True)
        case "VARIABLE_DISPLAY":
            value = retrieve(tokens[0][1])
            if value is None:
                print("No such variable.")
            else:
                print(value)
        case "ASSIGNMENT":
            tokens, name = token_strip(tokens)
            ast = build_ast(tokens)
            print(ast)
            store(ast, name)
        case "EQUATION":
            parse_equation(start_value)
        case "EXPRESSION":
            if tokens[1] == '?':
                display()
            elif tokens[0] == "FUNC_DEF":
                index = tokens[1].find("(")
                if index != -1:
                    name = tokens[1][:index]
                else:
                    raise IndexError("x of function couldn't be found.")
                data = retrieve(name, True)
                print(f"displaying curve for function {name} ...")
                display_curve(data, name)
            elif tokens[0] == "FUNC_CALL":
                start = tokens[1].find("(")
                end = tokens[1].find(")")
                if start == -1 or end == -1 or start == end:
                    raise IndexError("x of function couldn't be found.")
                name = tokens[1][:start]
                value = Complex(float(tokens[1][start + 1:end]))
                ast = retrieve(name, isFunction=True)
                result = ast.solve(value)
                print(result)
            else:
                ast = build_ast(tokens)
                print(ast)
                if isinstance(ast, tuple):  # If build_ast returned (Node, index)
                    ast = ast[0]
                if isinstance(ast, Node):
                    result = ast.solve()
                    print(result)
        case _:
            print(f"Unknown value : {type}. Tokens :\n{tokens}")