"""Class to hold equations"""

from ft_maths import ft_sqrt
from fractions import Fraction
from Polynomial import Polynomial

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

class Equation():
    def __init__(self, a, b, c, ra = None, rb = None, rc = None):
        self._deg0 = a
        self._deg1 = b
        self._deg2 = c
        if ra is None:
            ra = Polynomial(0, 0)  
        self._res0 = ra
        if rb is None:
            rb = Polynomial(0, 1)    
        self._res1 = rb
        if rc is None:
            rc = Polynomial(0, 2)   
        self._res2 = rc

    def left_side(self):
        """Returns the left side of the equation
        as a string.
        
        Returns:
            str: left side of the equation."""
        if self._deg0.coeff == 0 and self._deg1.coeff == 0 and self._deg2.coeff == 0:
            return "0"
        value = "" if self._deg0.coeff > 0 else "-" if self._deg0.coeff < 0 else ""
        value += str(self._deg0)
        if self._deg0.coeff == 0:
            value += "" if self._deg1.coeff > 0 else "-" if self._deg1.coeff < 0 else ""
            value += str(self._deg1)
        else:
            value += " + " if self._deg1.coeff > 0 else " - " if self._deg1.coeff < 0 else ""
            value += str(self._deg1)
        if self._deg1.coeff == 0 and self._deg0.coeff == 0:
            value += "" if self._deg2.coeff > 0 else "-" if self._deg2.coeff < 0 else ""
            value += str(self._deg2)
        else:
            value += " + " if self._deg2.coeff > 0 else " - " if self._deg2.coeff < 0 else ""
            value += str(self._deg2)
        return value

    def right_side(self):
        """Returns the right side of the equation
        as a string.
        
        Returns:
            str: right side of the equation."""
        if self._res0.coeff == 0 and self._res1.coeff == 0 and self._res2.coeff == 0:
            return "0"
        value = "" if self._res0.coeff > 0 else "-" if self._res0.coeff < 0 else ""
        value += str(self._res0)
        if self._res0.coeff == 0:
            value += "" if self._res1.coeff > 0 else "-" if self._res1.coeff < 0 else ""
            value += str(self._res1)
        else:
            value += " + " if self._res1.coeff > 0 else " - " if self._res1.coeff < 0 else ""
            value += str(self._res1)
        if self._res1.coeff == 0 and self._res0.coeff == 0:
            value += "" if self._res2.coeff > 0 else "-" if self._res2.coeff < 0 else ""
            value += str(self._res2)
        else:
            value += " + " if self._res2.coeff > 0 else " - " if self._res2.coeff < 0 else ""
            value += str(self._res2)
        return value

    def __str__(self):
        return (self.left_side() + " = " + self.right_side()).replace(".0 ", ' ').replace(".0x", 'x').replace(".0\n", '\n')
    
    def degree(self) -> int:
        """Returns the polynomial degree of the equation as a string.
        
        Returns:
            int : polynomial degree"""
        deg_right = max(max(self._deg0.degree(), self._deg1.degree()), self._deg2.degree())
        deg_left = max(max(self._res0.degree(), self._res1.degree()), self._res2.degree())
        return max(deg_right, deg_left)

    def reorder(self):
        """Reorders the equation in the a + bx + cx^2 = d format"""
        flag = False
        #left side
        if self._deg0.exponant > self._deg1.exponant:
            backup = self._deg0
            self._deg0 = self._deg1
            self._deg1 = backup
            flag = True
        if self._deg0.exponant > self._deg2.exponant:
            backup = self._deg0
            self._deg0 = self._deg2
            self._deg2 = backup
            flag = True
        if self._deg1.exponant > self._deg2.exponant:
            backup = self._deg1
            self._deg1 = self._deg2
            self._deg2 = backup
            flag = True
        #Right side
        if self._res0.exponant > self._res1.exponant:
            backup = self._res0
            self._res0 = self._res1
            self._res1 = backup
            flag = True
        if self._res0.exponant > self._res2.exponant:
            backup = self._res0
            self._res0 = self._res2
            self._res2 = backup
            flag = True
        if self._res1.exponant > self._res2.exponant:
            backup = self._res1
            self._res1 = self._res2
            self._res2 = backup
            flag = True
        if flag is True:
            self.reorder()

    def simplify_left(self, coeff, expo, sign):
        value = self.left_side()
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
        value = self.right_side()
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
        if self._res0.coeff < 0:
            self.simplify_step(self._res0.coeff, 0, '+')
            coeff = self._deg0.coeff + self._res0.coeff
            self._res0 = Polynomial(0, 0)
            self._deg0 = Polynomial(coeff, 0)
        elif self._res0.coeff > 0:
            coeff = self._deg0.coeff - self._res0.coeff
            self.simplify_step(self._res0.coeff, 0, '-')
            self._res0 = Polynomial(0, 0)
            self._deg0 = Polynomial(coeff, 0)
        
        if self._res1.coeff < 0:
            coeff = self._deg1.coeff + self._res1.coeff
            self.simplify_step(self._res1.coeff, 1, '+')
            self._res1 = Polynomial(0, 1)
            self._deg1 = Polynomial(coeff, 1)
        elif self._res1.coeff > 0:
            coeff = self._deg1.coeff - self._res1.coeff
            self.simplify_step(self._res1.coeff, 1, '-')
            self._res1 = Polynomial(0, 1)
            self._deg1 = Polynomial(coeff, 1)

        if self._res2.coeff < 0:
            coeff = self._deg2.coeff + self._res2.coeff
            self.simplify_step(self._res2.coeff, 2, '+')
            self._res2 = Polynomial(0, 2)
            self._deg2 = Polynomial(coeff, 2)
        elif self._res2.coeff > 0:
            coeff = self._deg2.coeff - self._res2.coeff
            self.simplify_step(self._res2.coeff, 2, '-')
            self._res2 = Polynomial(0, 2)
            self._deg2 = Polynomial(coeff, 2)

    def solve(self):
        """Solves the equation."""
        if self._deg1.coeff == 0 and self._deg2.coeff == 0: #Not an equation (a=b)
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
                print(f"({format_complex(x1)}, {format_complex(x2)})")

    def run(self):
        """Runs the whole sequence."""
        print(f"Base equation     : {str(self)}")
        print(f"Polynomial degree : {str(self.degree())}")
        self.reorder()
        print(f"Ordered Equation  : {str(self)}")
        self.simplify()
        print(f"Reduced equation  : {str(self)}")
        self.solve()