"""Class for storing matrixes."""

from maths.Complex import Complex

class Matrix():
    """Creates a Matrix."""
    def __init__(self, values, readFromTokens = True):
        if readFromTokens:
            self._values = [[]]
            self.read(values)
        else:
            self._values = values

    def __str__(self):
        result = ""
        for data in self._values:
            result += "["
            for i in range(len(data)):
                if i + 1 >= len(data):
                    result += f"{data[i]}"
                else:
                    result += f"{data[i]}, "
            result += "]\n"
        return result.strip()

    def read(self, value):
        if value is None:
            return
        rows = value[2:-2].split("];[")  # Remove outer brackets and split rows
        self._values = [
            [Complex(int(num.strip()), 0) for num in row.split(',')]  # Convert each entry to a Complex number
            for row in rows
        ]
    
    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise AttributeError("You can only add a Matrix to another one !")
        return Matrix([[self._values[i][j] + other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))], False)
    
    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise AttributeError("You can only substract a Matrix to another one !")
        return Matrix([[self._values[i][j] - other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))], False)
    
    def __mul__(self, other):
        if isinstance(other, (int, float, Complex)):
            return Matrix([[val * other for val in row] for row in self._values], False)
        return Matrix([[self._values[i][j] * other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))], False)
    
    def __mod__(self, other):
        if not isinstance(other, Matrix):
            raise AttributeError("You can only modulo a Matrix to another one !")
        return Matrix([[val % other for val in row] for row in self._values], False)
    
    def __pow__(self, other):
        if isinstance(other, int):
            result = self
            for _ in range(other - 1):
                result = result * self
            return result
        raise AttributeError("You can only power a Matrix with a positive integer !")
    
    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise AttributeError("You can only use ** between two Matrices !")
        return Matrix([[sum(self._values[i][k] * other._values[k][j] for k in range(len(self._values[0]))) for j in range(len(other._values[0]))] for i in range(len(self._values))], False)
    
    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value
