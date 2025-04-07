"""A class to store the Abstract Syntax Tree"""

from config import retrieve

from maths.Complex import Complex
from maths.Matrix import Matrix

precedence = {
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2,
    '^': 3, '**': 3
}

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
        if self.left is None and self.right is None:
            if self.value == 'x' and x is not None:
                return x
            elif self.value == 'x' and x is None:
                raise ValueError("x used outside of an equation or a function !")
            return self.value
        left_value = self.left.solve()
        right_value = self.right.solve()
        match (self.value):
            case '+':
                return left_value + right_value
            case '-':
                return left_value - right_value
            case '*':
                return left_value * right_value
            case '/':
                return left_value / right_value
            case '%':
                return left_value % right_value
            case '^':
                return left_value ** right_value
            case '**':
                if isinstance(left_value, Matrix):
                    return left_value @ right_value
                else:
                    return left_value ** right_value
            case _:
                raise AttributeError(f"Unknown operator {self.value} !")

def parse_expr(index, tokens, min_precedence=1):
    token = tokens[index]
    if not isinstance(token, tuple) and not isinstance(token, list):
        if tokens[0] == 'VAR':
            return retrieve(tokens[1]).solve()
        else:
            return Node(token), index
    if isinstance(token, list):
        left = build_ast(token)
    else:
        token_type, token_value = token
        if token_type == "INTEGER":
            left = Node(Complex(int(token_value), 0))
        elif token_type == "DECIMAL":
            left = Node(Complex(float(token_value), 0))
        elif token_type == "COMPLEX":
            left = Node(Complex(0, int(token_value[:-1])))
        elif token_type == "MATRIX":
            left = Node(Matrix(token_value))
        elif token_type in ("VAR", "FUNC_CALL"):
            if token_type == 'x':
                left = Node('x')
            else:
                left = Node(retrieve(token_value).solve())
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
        next_min_precedence = precedence[op_value] + (1 if op_value in ['^', '**'] else 0)
        right, index = parse_expr(index, tokens, next_min_precedence)
        left = Node(op_value, left, right)
    return left, index

def build_ast(tokens):
    if isinstance(tokens, tuple):  
        return parse_expr(1, tokens)[0]
    return parse_expr(0, tokens)[0]
