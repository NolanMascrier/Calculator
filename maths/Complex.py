"""Class for complexes values."""

class Complex():
    """Creates a complex number."""
    def __init__(self, real, im):
        self._real = real
        self._imag = im

    def __str__(self):
        if self.imag == 0 and self.real == 0:
            return "0"
        if self.imag == 0:
            return str(self._real)
        if self.real == 0:
            return ("" if self.imag >= 0 else "-") + str(abs(self.imag)) + "i"
        return str(self.real) + ("+" if self.imag >= 0 else "-") + str(abs(self.imag)) + "i"

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
    
    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(self.real * other.real - self.imag * other.imag, self.real * other.imag + self.imag * other.real)
        elif isinstance(other, (int, float)):
            return Complex(self.real * other, self.imag * other)
        return None
    
    def __rmul__(self, other):
        return self * other
    
    def __mod__(self, other):
        return Complex(self.real % other, self.imag % other) if isinstance(other, (int, float)) else None
    
    def __pow__(self, other):
        if isinstance(other, Complex) and other.imag == 0:
            result = Complex(1, 0)
            for _ in range(other.real):
                result *= self
            return result
        raise ValueError("Unsupported value for power")
    
    def read(self, value):
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