"""A class to store the Abstract Syntax Tree"""

from storage import retrieve

from ft_parser import tokenize, parse
from maths.complex import Complex
from maths.matrix import Matrix
from equations.ft_maths import IS_MATHS, IS_VARIABLE

precedence = {
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2,
    '^': 3, '**': 3
}

#helper functions for reducing
def _is_var(node, name):
    return isinstance(node, Node) and node.left is None\
        and node.right is None and node.value == name

def _is_mul(node, var_name):
    return (
        isinstance(node, Node)
        and node.value == '*'
        and ((_is_var(node.left, var_name) and isinstance(node.right.value, Complex)) or
             (_is_var(node.right, var_name) and isinstance(node.left.value, Complex)))
    )

def _extract_coef(node, var_name):
    if _is_var(node.left, var_name) and isinstance(node.right.value, Complex):
        return node.right.value.real
    if _is_var(node.right, var_name) and isinstance(node.left.value, Complex):
        return node.left.value.real
    return 1

def pseudo_execute(execute_type, tokens):
    """A pseudo execution to use inside function calls. To handle cases such as 
    f(3 + 4), f(4i), or even f(g(x)). 
    
    Args:
        execute_type (string): Type of the command. Can be FUNC_DEF, VARIABLE_DISPlAY, \
        ASSIGNMENT, EQUATION or EXPRESSION.
        tokens (list|tuple): list of tokens to use. Can also be a single tuple \
        in some cases. 
        start_value (str): backup of the original input. Only used for equation \
        solving.
    
    Returns:
        (Complex|None): Returns the computed value. If the command yields no result\
        (ie function assignment), returns None.
    """
    match(execute_type):
        case "VARIABLE_DISPLAY":
            if tokens[0][1] in IS_VARIABLE:
                return IS_VARIABLE[tokens[0][1]]
            return retrieve(tokens[0][1])
        case "EXPRESSION":
            if tokens[1] == '?':
                return None
            elif tokens[0] == "FUNC_DEF":
                return None
            else:
                ast = build_ast(tokens)
                if isinstance(ast, tuple):  # If build_ast returned (Node, index)
                    ast = ast[0]
                if isinstance(ast, Node):
                    result = ast.solve()
                    return result
                return ast
        case _:
            return None

class FunctionCall:
    """Stores Function calls."""
    def __init__(self, ast, value):
        self.ast = ast
        self.value = value

    def __str__(self):
        return f"{self.ast}({self.value})"

class Node:
    """Abstract Syntax Tree class."""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.left and self.right:
            return f"({self.left} {self.value} {self.right})"
        return str(self.value)

    def solve(self, x = None):
        """Solves the node, calling itself recursirvely if
        one of the leafs is another node.
        
        Args:
            x (any): value for x in case of a function solving. \
            defaults to None.
        
        Raises:
            ValueError : x is used outside of an equation solving.
            AttributeError: unknown operator was used. Will only trigger \
            for `?`, as it is a pseudo-operator used for variable displaying.
            
        Returns:
            (Complex | Matrix) : computed result either as a Complex or \
            a Matrix.
        """
        if isinstance(self.value, FunctionCall):
            return self.value.ast.solve(self.value.value)
        if self.left is None and self.right is None:
            if self.value == 'x' and x is not None:
                return x
            elif self.value == 'x' and x is None:
                raise ValueError("x used outside of an equation or a function !")
            return self.value
        left_value = self.left.solve(x)
        right_value = self.right.solve(x)
        match (self.value):
            case '^':
                return left_value ** right_value
            case '**':
                if isinstance(left_value, Matrix):
                    return left_value @ right_value
                else:
                    return left_value ** right_value
            case '*':
                return left_value * right_value
            case '/':
                return left_value / right_value
            case '%':
                return left_value % right_value
            case '+':
                return left_value + right_value
            case '-':
                return left_value - right_value
            case _:
                raise AttributeError(f"Unknown operator {self.value} !")

    def reduce(self):
        """Reduces the tree to a simplest form.
        ie, x + 2x becomes 3x, 2 + x - 1 becomes x + 1, etc"""
        if isinstance(self.value, FunctionCall):
            return Node(FunctionCall(self.value.ast.reduce(), self.value.value))
        if self.left is None and self.right is None:
            return self
        if self.value in ('+', '-'):
            left = self.left.reduce()
            right = self.right.reduce()
            if self.value == '+' and isinstance(left.value, Complex)\
                    and not isinstance(right.value, Complex):
                left, right = right, left
            if left.value == '+' and isinstance(left.right.value, Complex)\
                    and isinstance(right.value, Complex):
                new_const = left.right.value + right.value if self.value == '+'\
                    else left.right.value - right.value
                return Node('+', left.left, Node(new_const)).reduce()
            if right.value == '+' and isinstance(right.right.value, Complex)\
                    and isinstance(left.value, Complex):
                new_const = left.value + right.right.value if self.value == '+'\
                    else left.value - right.right.value
                return Node('+', right.left, Node(new_const)).reduce()
            if left.value == '+' and isinstance(left.right.value, Complex)\
                    and isinstance(right.value, Complex) and self.value == '-':
                new_const = left.right.value - right.value
                return Node('+', left.left, Node(new_const)).reduce()
            if isinstance(left.value, Complex) and isinstance(right.value, Complex):
                return Node(Node(self.value, left, right).solve())
            if self.value == '+':
                if _is_var(left, 'x') and _is_mul(right, 'x'):
                    coef = _extract_coef(right, 'x')
                    return Node('*', Node(Complex(coef + 1)), Node('x')).reduce()
                elif _is_mul(left, 'x') and _is_var(right, 'x'):
                    coef = _extract_coef(left, 'x')
                    return Node('*', Node(Complex(coef + 1)), Node('x')).reduce()
                elif _is_mul(left, 'x') and _is_mul(right, 'x'):
                    coef = _extract_coef(left, 'x') + _extract_coef(right, 'x')
                    return Node('*', Node(Complex(coef)), Node('x')).reduce()
            return Node(self.value, left, right)
        left = self.left.reduce()
        right = self.right.reduce()
        if isinstance(left.value, Complex) and isinstance(right.value, Complex):
            return Node(Node(self.value, left, right).solve())
        if self.value == '*' and isinstance(right.value, Complex):
            if right.value == Complex(1):
                return left
            elif right.value == Complex(0):
                return Node(Complex(0))
        if self.value == '*' and isinstance(left.value, Complex):
            if left.value == Complex(1):
                return right
            elif left.value == Complex(0):
                return Node(Complex(0))
        if self.value == '+' and isinstance(left.value, Complex) and left.value == Complex(0):
            return right
        if self.value == '+' and isinstance(right.value, Complex) and right.value == Complex(0):
            return left

        return Node(self.value, left, right)

def builder(index, tokens, min_precedence=1):
    """Recursively parses the token list to create the \
    Abstract Syntax Tree.

    Args:
        index (int): curent index in the tree. 
        tokens (list | tuple): The list of tokens. Can be a \
        singular tuple in some cases.
        min_precedence (int, optionnal) : Minimum precedence found. \
        Defaults to 1.
    
    Returns:
        (Node, int): returns the Tree and the last updated index for \
        recursive use.
    """
    token = tokens[index]

    if not isinstance(token, tuple) and not isinstance(token, list):
        if tokens[0] == 'VAR':
            if tokens[1] in IS_VARIABLE:
                return IS_VARIABLE[tokens[1]]
            else:
                return retrieve(tokens[1]).solve()
        if tokens[0] == "FUNC_CALL":
            start = tokens[1].find("(")
            end = tokens[1].rfind(")")
            if start == -1 or end == -1 or start == end:
                raise IndexError("Value for x of function call couldn't be found.")
            value = tokens[1][start + 1:end]
            try:
                f_value = Complex(float(value))
            except ValueError:
                new_tokens = tokenize(value)
                parsed = parse(new_tokens)
                f_value = pseudo_execute(parsed["type"], parsed["tokens"])
            func_name = tokens[1][:start]
            if func_name in IS_MATHS:
                final_value = IS_MATHS[func_name](f_value)
                return final_value
            else:
                result = retrieve(func_name, True).solve(f_value)
                return result
        return Node(token), index

    left = 0
    if isinstance(token, list):
        left = build_ast(token)
    else:
        token_type, token_value = token
        if token_type == "INTEGER":
            left = Node(Complex(int(token_value)))
        elif token_type == "DECIMAL":
            left = Node(Complex(float(token_value)))
        elif token_type == "COMPLEX":
            left = Node(Complex(0, int(token_value[:-1])))
        elif token_type == "MATRIX":
            left = Node(Matrix(token_value))
        elif token_type in ("VAR", "FUNC_CALL"):
            if token_value == 'x':
                left = Node('x')
            elif token_type == "VAR":
                if token_value in IS_VARIABLE:
                    left = Node(IS_VARIABLE[token_value])
                else:
                    left = Node(retrieve(token_value).solve())
            elif token_type == "FUNC_CALL":
                start = token_value.find("(")
                end = token_value.find(")")
                if start == -1 or end == -1 or start == end:
                    raise IndexError("Value for x of function call couldn't be found.")
                value = token_value[start + 1:end]
                try:
                    f_value = Complex(float(value))
                except ValueError:
                    new_tokens = tokenize(value)
                    parsed = parse(new_tokens)
                    f_value = pseudo_execute(parsed["type"], parsed["tokens"])
                func_name = token_value[:start]
                if func_name in IS_MATHS:
                    final_value = IS_MATHS[func_name](f_value)
                    left = Node(final_value)
                else:
                    ast = retrieve(func_name, True)
                    left = Node(FunctionCall(ast, f_value))
        else:
            left = Node(token_value)
    index += 1
    while index < len(tokens):
        if isinstance(tokens[index], list):
            break
        op_type, op_value = tokens[index]
        if op_type != "OP":
            break
        if precedence[op_value] < min_precedence:
            break
        index += 1
        if op_value in ['^', '**']:
            next_min_precedence = precedence[op_value]
        else:
            next_min_precedence = precedence[op_value] + 1
        right, index = builder(index, tokens, next_min_precedence)
        left = Node(op_value, left, right)
    return left, index

def build_ast(tokens):
    """Inits the index for the builder, and returns the resulting \
    tree.
    
    Args:
        tokens (list | tuple) : The list of tokens. Can be a \
        single tuple in some cases.
    
    Returns:
        Node : built tree, ready to be solved or stored.
    """
    if isinstance(tokens, tuple):
        return builder(1, tokens)
    return builder(0, tokens)[0]
