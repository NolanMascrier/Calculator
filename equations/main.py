import sys
#Beurk le regex
import re
from Polynomial import Polynomial
from Equation import Equation

def extract_terms(expression, regex):
        """Extracts the Polynomials according to the regex"""
        terms = []
        for match in regex.finditer(expression):
            coeff_str, x_part, exponent_str = match.groups()
            if not coeff_str and not x_part:  
                continue
            if coeff_str == '' or coeff_str == '+':
                coeff = 1.0
            elif coeff_str == '-':
                coeff = -1.0
            else:
                coeff = float(coeff_str)
            exponent = int(exponent_str) if exponent_str else (1 if x_part else 0)
            if (exponent > 2):
                return None
            terms.append(Polynomial(coeff, exponent))
        return terms

def parse(equation):
    """Parses the equation and creates the polynomials using regex"""
    equation = equation.replace(" ", "")
    left, right = equation.split("=")
    if left == "" or right == "":
        print("The equation needs at least one element on each side of the = !")
        return
    regex = re.compile(r"([+-]?[0-9]*\.?[0-9]*)([xX](?:\^([0-9]+))?)?") #Thank you google
    left_terms = extract_terms(left, regex)
    right_terms = extract_terms(right, regex)
    to_solve = Equation(left_terms, right_terms)
    to_solve.run()

if __name__ == "__main__":
    try:
        eq = sys.argv[1]
        print(f"Input value       : {eq}")
        eq = eq.strip().replace(" ", '').replace("*", '')
        print(f"Stripped value    : {eq}")
        equals = eq.count('=')
        if equals < 1:
            print("An equation needs an equality, it's in the name")
        elif equals > 1:
            print("An equation needs a single equality !")
        else:
            parse(eq)
    except IndexError:
        print("You must put an equation for the program to work !")