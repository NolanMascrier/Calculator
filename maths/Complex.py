"""Class for complexes values."""

class Complex():
    """Creates a complex number.
    
    Args:
        real (float): Real part of the complex.
        im (float, optionnal): Imaginary part of the complex. Defaults to 0."""
    def __init__(self, real, im = 0):
        self._real = real
        self._imag = im

    def __str__(self):
        if self._imag == 0 and self._real == 0:
            return "0"
        if self._imag == 0:
            return str(self._real)
        if self._real == 0:
            return ("" if self._imag >= 0 else "-") + (str(abs(self._imag)) if abs(self._imag) != 1 else "") + "i"
        return str(self._real) + ("+" if self._imag >= 0 else "-") + (str(abs(self._imag)) if abs(self._imag) != 1 else "") + "i"

    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self._real + other._real, self._imag + other._imag)
        elif isinstance(other, (int, float)):
            return Complex(self._real + other, self._imag)
        return None
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self._real - other._real, self._imag - other._imag)
        elif isinstance(other, (int, float)):
            return Complex(self._real - other, self._imag)
        return None
    
    def __rsub__(self, other):
        return Complex(other - self._real, -self._imag)

    def __truediv__(self, other):
        """\/ operator overload.

        Raises: 
            ZeroDivisionError: Attempting to divide by zero.
        """
        if isinstance(other, Complex):
            a, b = self._real, self._imag
            c, d = other._real, other._imag
            denominator = c * c + d * d
            if denominator == 0:
                raise ZeroDivisionError("division by zero")
            return Complex((a * c + b * d) / denominator, (b * c - a * d) / denominator)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return Complex(self._real / other, self._imag / other)
        return None
    
    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(self._real * other._real - self._imag * other._imag, self._real * other._imag + self._imag * other._real)
        elif isinstance(other, (int, float)):
            return Complex(self._real * other, self._imag * other)
        return None
    
    def __rmul__(self, other):
        return self * other
    
    def __mod__(self, other):
        return Complex(self._real % other, self._imag % other) if isinstance(other, (int, float)) else None
    
    def _pow_int(self, n):
        """Handles integer exponentiation."""
        result = Complex(1, 0)
        base = self
        while n > 0:
            if n % 2 == 1:
                result *= base
            base *= base
            n //= 2
        return result

    def __pow__(self, other):
        if isinstance(other, Complex) and other._imag == 0:
            result = Complex(1, 0)
            for _ in range(other._real):
                result *= self
            return result
        raise ValueError("Unsupported value for power")
    
    def __rpow__(self, other):
        if self._imag != 0:
            raise ValueError("Unsupported value for power")
        result = Complex(1, 0)
        for _ in range(round(self._real)):
            result *= self
        return result

    def __lt__(self, other):
        if isinstance(other, (int, float)):
            other = Complex(other)
        if not isinstance(other, Complex):
            raise ValueError("cannot compare those two values")
        if self._real < other.real:
            return True
        return False 
    
    def read(self, value):
        """Reads a Complex number from a token.
        
        Args:
            value: Token to read.
            
        Raises:
            ValueError: Unknown token.
        """
        if value[0] == "INTEGER":
            self._real = int(value[1])
            self._imag = 0
        elif value[0] == "COMPLEX":
            self._real = 0
            self._imag = int(value[1][:-1])  # Remove 'i' and convert to int
        elif value[0] == "DECIMAL":
            self._real = float(value[1])
            self._imag = 0
        else:
            raise ValueError("Unsupported token type for Complex")

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