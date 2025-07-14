"""A class to store the Abstract Syntax Tree"""

from storage import retrieve

from ft_parser import tokenize, parse
from maths.complex import Complex
from maths.matrix import Matrix
from equations.ft_maths import IS_MATHS, IS_VARIABLE, ft_fact

precedence = {
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2,
    '^': 3, '**': 3
}

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

class FunctionStore:
    """Stores a function name and value."""
    def __init__(self, name, value = 'x'):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}({self.value})"

class Node:
    """Abstract Syntax Tree class."""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.left and self.right:
            if self.value == '*' and self.right.value == 'x':
                return f"({self.left}{self.right})"
            return f"({self.left} {self.value} {self.right})"
        return str(self.value)

    def is_constant(self):
        """Checks whether or not the node is a leaf."""
        return isinstance(self.value, Complex) and self.left is None and self.right is None

    def is_var(self):
        """Checks whether or not the node is a variable node."""
        return self.value == "x" and self.left is None and self.right is None

    def is_zero(self):
        """Checks if the node is a 0."""
        return self.is_constant() and self.value == 0

    def is_one(self):
        """Checks if the node is 1."""
        return self.is_constant() and self.value == 1

    def same_var(self, other):
        """Checks if the two nodes are two xs."""
        return self.is_var() and other.is_var() and self.value == other.value

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
        if isinstance(self.value, FunctionStore):
            return retrieve(self.value.name, True).solve(x)
        if self.left is None and self.right is None:
            if self.value == 'x' and x is not None:
                return x
            elif self.value == 'x' and x is None:
                raise ValueError("x used outside of an equation or a function !")
            return self.value
        left_value = self.left.solve(x)
        right_value = self.right.solve(x)
        match self.value:
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
        """Recuehfuhefuhefuzvnr"""
        if self.left is None and self.right is None:
            return self
        left = self.left.reduce()
        right = self.right.reduce()
        match self.value:
            case '+':
                if left.is_constant() and right.is_constant():
                    return Node(left.value + right.value)
                if left.is_zero():
                    return right
                if right.is_zero():
                    return left
                if left.value == '+' and left.right.is_constant() and right.is_constant():
                    return Node('+', Node(left.left, None, None),\
                        Node(left.right.value + right.value))
                return Node('+', left, right)
            case '*':
                # constant * constant
                if left.is_constant() and right.is_constant():
                    return Node(left.value * right.value)
                if left.is_zero() or right.is_zero():
                    return Node(Complex(0))
                if left.is_one():
                    return right
                if right.is_one():
                    return left
                if left.same_var(right):
                    return Node('^', left, Node(Complex(2)))
                if left.value == '^' and left.left.same_var(right) and left.right.is_constant():
                    return Node('^', right, Node(left.right.value + 1))
                if right.value == '^' and right.left.same_var(left) and right.right.is_constant():
                    return Node('^', left, Node(right.right.value + 1))
                return Node('*', left, right)
            case '^':
                if left.is_constant() and right.is_constant():
                    return Node(left.value ** right.value)
                if right.is_zero():
                    return Node(Complex(1))
                if right.is_one():
                    return left
                if left.value == '^':
                    return Node('^', left.left, Node('*', left.right, right).reduce())
                return Node('^', left, right)
            case '-':
                if left.is_constant() and right.is_constant():
                    return Node(left.value - right.value)
                if right.is_zero():
                    return left
                return Node('-', left, right)
            case '/':
                if left.is_constant() and right.is_constant():
                    return Node(left.value / right.value)
                if right.is_one():
                    return left
                return Node('/', left, right)
            case _:
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
        if tokens[0] == "MATRIX":
            return Matrix(tokens[1], True)
        if tokens[0] == "FACT":
            cmp = Complex(0)
            cmp.read(tokens)
            return Complex(ft_fact(cmp))
        if tokens[0] == "COMPLEX":
            cmp = Complex(0)
            cmp.read(tokens)
            return cmp
        if tokens[0] == "FUNC_DEF":
            start = tokens[1].find("(")
            end = tokens[1].rfind(")")
            if start == -1 or end == -1 or start == end:
                raise IndexError("Value for x of function call couldn't be found.")
            value = tokens[1][start + 1:end]
            func_name = tokens[1][:start]
            return FunctionStore(func_name, value)
        if tokens[0] == 'VAR':
            if tokens[1] in IS_VARIABLE:
                return IS_VARIABLE[tokens[1]]
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
                result = retrieve(func_name, True)
                result = result.solve(f_value)
                return result
        return Node(token), index

    left = 0
    if isinstance(token, list):
        left = build_ast(token)
    else:
        token_type, token_value = token
        if token_type == "FACT":
            left = Node(Complex(ft_fact(float(token_value[:len(token_value)-1]))))
        elif token_type == "INTEGER":
            left = Node(Complex(int(token_value)))
        elif token_type == "DECIMAL":
            left = Node(Complex(float(token_value)))
        elif token_type == "COMPLEX":
            left = Node(Complex(0, 0))
            left.value.read(token)
        elif token_type == "MATRIX":
            left = Node(Matrix(token_value))
        elif token_type == "FUNC_DEF":
            start = token_value.find("(")
            end = token_value.rfind(")")
            if start == -1 or end == -1 or start == end:
                raise IndexError("Value for x of function call couldn't be found.")
            value = token_value[start + 1:end]
            func_name = token_value[:start]
            left = Node(FunctionStore(func_name, value))
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
