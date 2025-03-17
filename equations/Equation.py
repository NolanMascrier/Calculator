"""Class to hold equations"""

from ft_maths import ft_sqrt
from fractions import Fraction
from Polynomial import Polynomial

MAX_DEGREE = 2

def format_fraction(value, max_denominator = 100):
    """Displays the fraction if it's reductible, displays the
    float otherwise.
    
    Args:
        value (float): value to display.
        max_denominator (int): maximum value for the denominator.
        Defaults to 100.
    
    Returns:
        str: displayable value.
    """
    frac = Fraction.from_float(value).limit_denominator()
    if frac.denominator == 1:
        return frac.numerator
    return (frac) if frac.denominator <= max_denominator else round(value, 6)

def format_complex(complex):
    """Simple function to format the complex number.

    Args:
        complex (complex): complex number to format
    
    Returns:
        str: formatted complex number.
    """
    re = complex.real
    im = complex.imag
    fre = format_fraction(re)
    fim = format_fraction(abs(im))
    if im < 0:
        return str(fre) + " - " + str(fim) + "i"
    elif im > 0:
        return str(fre) + " + " + str(fim) + "i"
    else:
        return str(fre)
    
def squish(list):
    """Squishes a list of polynomials.
    
    Args:
        list (dict): the list of polymomials.

    Returns:
        dict: the squished list.    
    """
    seen_exponents = []
    result = []
    for obj in list:
        if obj.exponant in seen_exponents:
            for res_obj in result:
                if res_obj.exponant == obj.exponant:
                    res_obj.coeff += obj.coeff
                    break
        else:
            result.append(Polynomial(obj.coeff, obj.exponant))
            seen_exponents.append(obj.exponant)
    return result

class Equation():
    def __init__(self, left = None, right = None):
        if left is None:
            self._left = []
        else:
            self._left = left
        if right is None:
            self._right = []
        else:
            self._right = right
        self._deg_left = 0
        self._deg_right = 0
        self.__complete_missing()
        self._deg = max(self._deg_left, self._deg_right)
        #self.__squash()

    def __sort_sides(self):
        """Sorts left and right sides according to
        their degrees.
        """
        sorted_left = sorted(self._left, key= lambda data: data.exponant)
        sorted_right = sorted(self._right, key= lambda data: data.exponant)
        self._left = sorted_left
        self._right = sorted_right

    def __squash(self):
        """Squish all polynomial of the same degree together.
        """
        self._left = squish(self._left)
        self._right = squish(self._right)

    def __complete_missing(self):
        """Adds the missing polynomials that are equal
        to 0 in the equation."""
        got_left = []
        got_right = []
        for data in self._left:
            got_left.append(data.exponant)
        for data in self._right:
            got_right.append(data.exponant)
        max_left = max(got_left)
        max_right = max(got_right)
        self._deg_left = max_left
        self._deg_right = max_right
        max_equation = max(max_left, max_right)
        for i in range(0, max_equation + 1):
            if i not in got_left:
                self._left.append(Polynomial(0, i))
        for i in range(0, max_equation + 1):
            if i not in got_right:
                self._right.append(Polynomial(0, i))

    def __left_side(self):
        """Returns the left side of the equation
        as a string.
        
        Returns:
            str: left side of the equation."""
        if self._deg_left == 0:
            return "0"
        value = ""
        flag = False
        for data in self._left:
            if data.coeff == 0:
                continue

            if flag is False:
                sign = "" if data.coeff > 0 else "-"
                value += sign + str(data)
                flag = True
            else:
                sign = " + " if data.coeff > 0 else " - "
                value += sign + str(data)
        return value

    def __right_side(self):
        """Returns the right side of the equation
        as a string.
        
        Returns:
            str: right side of the equation."""
        if self._deg_right == 0:
            return "0"
        value = ""
        flag = False
        for data in self._right:
            if data.coeff == 0:
                continue

            if flag is False:
                sign = "" if data.coeff > 0 else "-"
                value += sign + str(data)
                flag = True
            else:
                sign = " + " if data.coeff > 0 else " - "
                value += sign + str(data)
        if value == "":
            return "0"
        return value

    def __str__(self):
        return (self.__left_side() + " = " + self.__right_side()).replace(".0 ", ' ').replace(".0x", 'x').replace(".0\n", '\n')
    
    def degree(self) -> int:
        """Returns the polynomial degree of the equation as a string.
        
        Returns:
            int : polynomial degree"""
        return self._deg

    def simplify_left(self, coeff, expo, sign):
        value = self.__left_side()
        index = value.find(f"x^{expo}")
        if expo == 0:
            index = value.find(' ')
            if index == -1:
                index = len(value)
            to_add = " (" + sign + " " + str(Polynomial(coeff, expo)) + ")"
            stepped = value[:index] + to_add + value[index:]
            return stepped
        if index == -1:
            index = len(value)
        to_add = " (" + sign + " " + str(Polynomial(coeff, expo)) + ")"
        stepped = value[:index + 3] + to_add + value[index + 3:]
        return stepped
    
    def simplify_right(self, coeff, expo, sign):
        value = self.__right_side()
        index = value.find(f"x^{expo}")
        if expo == 0:
            index = value.find(' ')
            if index == -1:
                index = len(value)
            to_add = " (" + sign + " " + str(Polynomial(coeff, expo)) + ")"
            stepped = value[:index] + to_add + value[index:]
            return stepped
        if index == -1:
            index = len(value)
        to_add = " (" + sign + " " + str(Polynomial(coeff, expo)) + ")"
        stepped = value[:index + 3] + to_add + value[index + 3:]
        return stepped

    def simplify_step(self, coeff, expo, sign):
        if coeff == 0:
            return
        value = self.simplify_left(coeff, expo, sign) + " = " + self.simplify_right(coeff, expo, sign)
        value = value.replace(".0 ", ' ').replace(".0x", 'x').replace(".0\n", '\n')
        print(f"Medium step       : {value}")

    def simplify(self):
        """Simplifies the equation by making the right side equal
        to 0."""
        for i in range(0, self._deg + 1):
            if self._right[i].coeff < 0:
                self.simplify_step(self._right[i].coeff, i, '+')
                coeff = self._left[i].coeff + self._right[i].coeff
                self._right[i] = Polynomial(0, i)
                self._left[i] = Polynomial(coeff, i)
            elif self._right[i].coeff > 0:
                self.simplify_step(self._right[i].coeff, i, '-')
                coeff = self._left[i].coeff - self._right[i].coeff
                self._right[i] = Polynomial(0, i)
                self._left[i] = Polynomial(coeff, i)

    def solve(self):
        """Solves the equation."""
        """if self._deg1.coeff == 0 and self._deg2.coeff == 0: #Not an equation (a=b)
            if self._res0.coeff == self._deg0.coeff:
                print("Any real number is a solution.")
            else:
                print("No Solutions !")
        elif self._deg2.coeff == 0: #equation is ax + b = y
            #ax = y - b
            right = self._deg0.coeff * -1
            #x = (y - b) / a
            if self._deg1.coeff == 0:
                print("No Solutions !")
                return
            right /= self._deg1.coeff
            soluce = right
            print(f"Solution          : {soluce}")
        else: #equation is ax^2 + bx + c = y
            #delta = b^2 - (4ac)
            discriminant = self._deg1.coeff  ** 2 - (4 * self._deg0.coeff * self._deg2.coeff)
            #Quadratic
            #x=(−b±sqrt(b2−4ac))/2c
            x1 = (-self._deg1.coeff + ft_sqrt(discriminant) ) / (2 * self._deg2.coeff)
            x2 = (-self._deg1.coeff - ft_sqrt(discriminant) ) / (2 * self._deg2.coeff)
            if discriminant == 0:
                print("Discriminant is equal to 0, only one solution is :")
                print(x1)
            elif discriminant > 0:
                print("Discriminant is strictly positive, the two solutions are:")
                print(f"({format_fraction(x1)}, {format_fraction(x2)})")
            elif discriminant < 0:
                print("Discriminant is strictly negative, the two complex solutions are :")
                print(f"({format_complex(x1)}, {format_complex(x2)})")"""

    def run(self):
        """Runs the whole sequence."""
        print(f"Base equation     : {str(self)}")
        self.__squash()
        print(f"Squashed equation : {str(self)}")
        print(f"Polynomial degree : {str(self.degree())}")
        if self.degree() > MAX_DEGREE:
            print(f"Degree is superior to {MAX_DEGREE}, cannot solve")
            return
        self.__sort_sides()
        print(f"Ordered Equation  : {str(self)}")
        self.simplify()
        print(f"Reduced equation  : {str(self)}")
        self.solve()