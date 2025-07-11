"""*You can't use math or cmath lib* whyyyyyyyyy"""

from maths.complex import Complex

PI = 3.141592653589793
E = 2.718281828459045

def ft_fact(n):
    """Returns the factorial of n.
    
    Args:
        n (int): n! value"""
    if isinstance(n, Complex):
        if n.imag != 0:
            raise ValueError("Complex numbers don't have factorials !")
        n = n.real
    if int(n) != n:
        raise ValueError("Decimal numbers don't have factorials !")
    if n < 0:
        raise ValueError("Negative numbers don't have factorials !")
    if n in [0, 1]:
        return 1
    sums = 1
    for i in range(2, n + 1):
        sums *= i
    return sums

def ft_sin(x):
    """Calculates sin(x)
    
    Args:
        x (float): Input value in RADIANS"""
    if isinstance(x, Complex):
        if x.imag != 0:
            raise ValueError("Cannot use sin on complex number !")
        x = x.real
    if x == PI:
        return 0
    sin_x = 0
    x = x % (2 * PI)
    if x > PI:
        x -= 2 * PI
    for n in range(15):
        term = ((-1) ** n) * (x ** (2 * n + 1)) / ft_fact(2 * n + 1)
        sin_x += term
    return sin_x

def ft_cos(x):
    """Calculates cos(x)
    
    Args:
        x (float): Input value in RADIANS"""
    if isinstance(x, Complex):
        if x.imag != 0:
            raise ValueError("Cannot use sin on complex number !")
        x = x.real
    if x == PI:
        return -1
    cos_x = ft_sin((PI / 2) - x)
    return cos_x

def ft_tan(x):
    """Calculates tan(x)
    
    Args:
        x (float): Input value in RADIANS"""
    if isinstance(x, Complex):
        if x.imag != 0:
            raise ValueError("Cannot use sin on complex number !")
        x = x.real
    if x == PI:
        return 0
    return ft_sin(x)/ft_cos(x)

def ft_sqrt(value):
    """Does a square root."""
    if isinstance(value, Complex):
        if value.imag != 0:
            raise ValueError("Cannot use sqrt on complex number !")
        value = value.real
    if value >= 0:
        return value ** 0.5
    return Complex(0, (-value) ** 0.5)

IS_MATHS = {
    "factorial": ft_fact,
    "sin": ft_sin,
    "cos": ft_cos,
    "tan": ft_tan,
    "sqrt": ft_sqrt
}

IS_VARIABLE = {
    "pi": PI,
    "π": PI,
    "e": E
}
