"""*You can't use math or cmath lib* whyyyyyyyyy"""
PI = 3.141592653589793

def ft_fact(n):
    """Returns the factorial of n.
    
    Args:
        n (int): n! value"""
    sum = 1
    for i in range(2, n + 1):
        sum *= i
    return sum

def ft_sin(x):
    """Calculates sin(x)
    
    Args:
        x (int)"""
    x = x % (2 * PI)
    if x > PI:
        x -= 2 * PI
    sin_x = 0
    for n in range(10):
        term = (-1 ** n) * (x ** (2 * n + 1)) / ft_fact(2 * n + 1)
        sin_x += term
    return sin_x

def ft_cos(x):
    """Calculates cos(x)
    
    Args:
        x (int)"""
    x = x % (2 * PI)
    if x > PI:
        x -= 2 * PI
    cos_x = 0
    for n in range(10):
        term = (-1 ** n) * (x ** (2 * n)) / ft_fact(2 * n)
        cos_x += term
    return cos_x

def ft_sqrt(value):
    """Does a square root."""
    if value >= 0:
        return value ** 0.5
    return Complex(0, (-value) ** 0.5)

class Complex():
    """Creates a complex number."""
    def __init__(self, real, im):
        self._real = real
        self._imag = im

    def __str__(self):
        return str(self.real) + ("+" if self.imag >= 0 else "-") + str(self.imag) + "i"

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, (int, float)):
            return Complex(self.real + other, self.imag)
        return None
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)
        elif isinstance(other, (int, float)):
            return Complex(self.real - other, self.imag)
        return None
    
    def __rsub__(self, other):
        return Complex(other - self.real, -self.imag)

    def __truediv__(self, other):
        if isinstance(other, Complex):
            a, b = self.real, self.imag
            c, d = other.real, other.imag
            denominator = c * c + d * d
            if denominator == 0:
                raise ZeroDivisionError("division by zero")
            return Complex((a * c + b * d) / denominator, (b * c - a * d) / denominator)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return Complex(self.real / other, self.imag / other)
        return None

    @property
    def real(self):
        return self._real

    @real.setter
    def real(self, value):
        self._real = value

    @property
    def imag(self):
        return self._imag

    @imag.setter
    def imag(self, value):
        self._imag = value