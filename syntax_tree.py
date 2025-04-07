"""A class to store the Abstract Syntax Tree"""

from config import retrieve

from maths.Complex import Complex
from maths.Matrix import Matrix

precedence = {
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2,
    '^': 3, '**': 3
}

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
            Complex | Matrix : computed result either as a Complex or \
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
            return retrieve(tokens[1]).solve()
        elif tokens[0] == "FUNC_CALL":
            start = tokens[1].find("(")
            end = tokens[1].find(")")
            if start == -1 or end == -1 or start == end:
                raise IndexError("Value for x of function call couldn't be found.")
            value = tokens[1][start + 1:end]
            return retrieve(tokens[1], True).solve(float(value))
        else:
            return Node(token), index
        
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
                left = Node(retrieve(token_value).solve())
            elif token_type == "FUNC_CALL":
                start = token_value.find("(")
                end = token_value.find(")")
                if start == -1 or end == -1 or start == end:
                    raise IndexError("Value for x of function call couldn't be found.")
                value = token_value[start + 1:end]
                ast = retrieve(token_value[:start], True)
                left = Node(FunctionCall(ast, Complex(float(value))))
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
