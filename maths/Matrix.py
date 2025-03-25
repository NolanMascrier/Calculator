"""Class for storing matrixes."""

from maths.Complex import Complex

class Matrix():
    def __init__(self, values):
        self._values = [[]]
        self.read(values)

    def __str__(self):
        result = ""
        for data in self._values:
            result += data + ",\n"
        return result
    
    def read(self, value):
        if value is None:
            return
        self._values = [[Complex(int(num), 0) for num in row.split(',')] for row in value[1:-1].split(';')]
    
    def __add__(self, other):
        return Matrix([[self._values[i][j] + other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))])
    
    def __sub__(self, other):
        return Matrix([[self._values[i][j] - other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))])
    
    def __mul__(self, other):
        if isinstance(other, (int, float, Complex)):
            return Matrix([[val * other for val in row] for row in self._values])
        return Matrix([[self._values[i][j] * other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))])
    
    def __mod__(self, other):
        return Matrix([[val % other for val in row] for row in self._values])
    
    def __pow__(self, other):
        if isinstance(other, int):
            result = self
            for _ in range(other - 1):
                result = result * self
            return result
        return None
    
    def __matmul__(self, other):
        return Matrix([[sum(self._values[i][k] * other._values[k][j] for k in range(len(self._values[0]))) for j in range(len(other._values[0]))] for i in range(len(self._values))])
    
    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value
