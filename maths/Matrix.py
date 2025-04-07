"""Class for storing matrixes."""

from maths.Complex import Complex

class Matrix():
    """Creates a Matrix.
    
    Args:
        values (str | list[list]): List of values to insert. Can be a token \
        or an actual matrix represented as a list of list.
        readFromTokens (bool, optionnal): Wether or not `values` if a token. Defaults to \
        `True`.

    Raises:
        AttributeError : The matrix's lines lengths are mistmatched. \
    """
    def __init__(self, values, readFromTokens = True):
        if readFromTokens:
            self._values = [[]]
            self.read(values)
        else:
            self._values = values
        self._lines = len(self._values)
        self._columns = len(self._values[0])
        for data in self._values:
            if len(data) != self._columns:
                raise AttributeError("A matrix needs the same amount of values on all lines !")

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
        """Reads a token and stores its values in the matrix.
        
        Args:
            value (string): Token to parse.
        """
        if value is None:
            return
        rows = value[2:-2].split("];[")
        self._values = [
            [Complex(float(num.strip()), 0) for num in row.split(',')]
            for row in rows
        ]

    def __identity_matrix(self, n):
        """Creates and returns an identity matrix of size n as a double list.
        An identity matrix of a matrix made of 0 and 1, only on the diagonal, eg : \n
        1 0 0 0 \n 
        0 1 0 0 \n
        0 0 1 0 \n
        0 0 0 1
        """
        matrix = self.__generate_empty_matrix(n, n)
        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 1
        return matrix
    
    def __add__(self, other):
        """\+ operator overload.
        
        Raises:
            AttributeError : An attempt to add a matrix with anything else was made.
            AttributeError : An attempt to add two matrices of different sizes was made.
        """
        if not isinstance(other, Matrix):
            raise AttributeError("You can only add a Matrix to another one !")
        if self._lines != other._lines or self._columns != other._columns:
            raise AttributeError("Two matrices needs the same amount of values to be added !")
        return Matrix([[self._values[i][j] + other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))], False)
    
    def __sub__(self, other):
        """\- operator overload.
        
        Raises:
            AttributeError : An attempt to substract a matrix with anything else was made.
            AttributeError : An attempt to substract two matrices of different sizes was made.
        """
        if not isinstance(other, Matrix):
            raise AttributeError("You can only substract a Matrix to another one !")
        if self._lines != other._lines or self._columns != other._columns:
            raise AttributeError("Two matrices needs the same amount of values to be substracted !")
        return Matrix([[self._values[i][j] - other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))], False)
    
    def __generate_empty_matrix(self, cols, lines):
        """Generates a matrix of size cols*line filled with 0s.
        
        Args:
            cols (int): Numbers of values per line.
            lines (int): Numbers of lines.
            
        Returns:
            list[list]: An empty matrix as a list."""
        reference = []
        matrix = []
        for _ in range(cols):
            reference.append(0)
        for _ in range(lines):
            matrix.append(reference.copy())
        return matrix

    def __mul__(self, other):
        """Makes a simple multiplication between two matrices or between a matrix
        and a scalar."""
        if isinstance(other, (int, float, Complex)):
            return Matrix([[val * other for val in row] for row in self._values], False)
        if not isinstance(other, Matrix):
            raise AttributeError("You can only (simple) multiply a matrix with a scalar or another matrix !")
        if self._columns != other._lines:
            raise AttributeError("Two matrices needs the same amount of values to be (simple) multiplied !")
        return Matrix([[self._values[i][j] * other.values[i][j] for j in range(len(self._values[0]))] for i in range(len(self._values))], False)
    
    def __mod__(self, other):
        """\% operator overload.
        
        Raises:
            AttributeError : An attempt to mod a matrix with anything else was made.
            AttributeError : An attempt to mod two matrices of different sizes was made.
        """
        if not isinstance(other, Matrix):
            raise AttributeError("You can only modulo a Matrix to another one !")
        if self._lines != other._lines or self._columns != other._columns:
            raise AttributeError("Two matrices needs the same amount of values to be moduled !")
        return Matrix([[val % other for val in row] for row in self._values], False)
    
    def __pow__(self, other):
        """\^ operator overload.
        
        Raises:
            AttributeError : An attempt to raise a matrix with anything else than an int.
            AttributeError : An attempt to raise a non square matrix was made."""
        if isinstance(other, int):
            if self._lines != self._columns:
                raise AttributeError("You can only raise a square matrix to a power !")
            result = self
            for _ in range(other - 1):
                result = result * self
            return result
        raise AttributeError("You can only power a Matrix with a positive integer !")
    
    def __matmul__(self, other):
        """@ operator overload. Multiplication of two matrices.

        Raises:
            AttributeError : An attempt to raise a matrix with anything else than an int.
            AttributeError : An attempt to raise a non square matrix was made.
        """
        if not isinstance(other, Matrix):
            raise AttributeError("You can only (true) multiply a matrix with another one !")
        if self._columns != other._lines:
            raise AttributeError("To multiply two matrices, the first one needs to have as many columns as the second one has lines !")
        matr = self.__generate_empty_matrix(self._columns, other._lines)
        for row in range(other._lines):
            for column in range(self._columns):
                for value in range(len(other.values)):
                    matr[row][column] += self._values[row][value] * other.values[value][column]
        return Matrix(matr, False)
    
    def __eq__(self, other):
        """Equality operator overload =="""
        if not isinstance(other, Matrix):
            return False
        if self._columns != other._columns or self._lines != other.lines:
            return False
        for i in range(self._columns):
            for j in range(self._lines):
                if self._values[i][j] != other._values[i][j]:
                    return False
        return True

    def __ne__(self, other):
        """Inquality operator overload !="""
        if not isinstance(other, Matrix):
            return True
        if self._columns != other._columns or self._lines != other.lines:
            return True
        if self == other:
            return False
        return True
    
    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value
    
    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value):
        self._lines = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
