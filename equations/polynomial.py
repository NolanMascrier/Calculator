"""Class to hold polynomials"""

class Polynomial():
    """Class to hold polynomials.
    
    Args:
        coeff (float): Coefficient of the polynomial. Defaults to 1
        exponant (float): Exponant of the polynomial. Defaults to 0
        variable (str): how to name the variable. Defaults to 'x'
    """
    def __init__(self, coeff = 1.0, exponant = 0.0, variable = 'x'):
        self._coeff = coeff
        self._exponant = exponant
        self._variable = variable

    def __str__(self) -> str:
        """Returns the polynomial as a
        string.
        
        Returns:
            str : Polynomial as a string."""
        if self._coeff == 0:
            return ""
        val = ""
        if self._exponant == 0:
            return str(abs(self._coeff))
        if abs(self._coeff) == 1:
            val += self._variable
        else:
            val += "" + str(abs(self._coeff)) + self._variable
        if self._exponant == 1:
            return val
        return val + "^" + str(self._exponant)

    def degree(self) -> int:
        """Returns the degree of the polynomial

        Returns:
            int : degree of the polynomial
        """
        return self._exponant

    def calculate(self, x) -> float:
        """Returns the result for a given x

        Args:
            x (float) : value for x

        Returns:
            float : computed result"""
        return self._coeff * (x ** self._exponant)

    @property
    def coeff(self):
        """Returns the coefficient of the polynomial."""
        return self._coeff

    @coeff.setter
    def coeff(self, value):
        self._coeff = value

    @property
    def exponant(self):
        """Returns the exponant of the polynomial."""
        return self._exponant

    @exponant.setter
    def exponant(self, value):
        self._exponant = value

    @property
    def variable(self):
        """Returns the variable's display name. Should
        be x in most cases."""
        return self._variable

    @variable.setter
    def variable(self, value):
        self._variable = value
