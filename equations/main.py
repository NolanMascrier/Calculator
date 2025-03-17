import sys
#Beurk le regex
import re
from Polynomial import Polynomial
from Equation import Equation

def extract_terms(expression, regex):
        """Extracts the tuples according to the regex"""
        terms = []
        seen_exponents = set()
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
            terms.append((coeff, exponent))
            seen_exponents.add(exponent)
        for exp in range(0, 3):
            if exp not in seen_exponents:
                terms.insert(exp, (0, exp))
        return terms

def parse(equation):
    """Parses the equation and creates the polynomials using regex"""
    equation = equation.replace(" ", "")
    left, right = equation.split("=")
    regex = re.compile(r"([+-]?[0-9]*\.?[0-9]*)(x(?:\^([0-9]+))?)?") #Thank you google
    left_terms = extract_terms(left, regex)
    right_terms = extract_terms(right, regex)
    if left_terms is None or right_terms is None:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return
    p0 = Polynomial(left_terms[0][0], left_terms[0][1])
    p1 = Polynomial(left_terms[1][0], left_terms[1][1])
    p2 = Polynomial(left_terms[2][0], left_terms[2][1])
    r0 = Polynomial(right_terms[0][0], right_terms[0][1])
    r1 = Polynomial(right_terms[1][0], right_terms[1][1])
    r2 = Polynomial(right_terms[2][0], right_terms[2][1])
    to_solve = Equation(p0, p1, p2, r0, r1, r2)
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