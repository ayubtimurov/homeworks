import sympy as sp
import numpy as np
import math

x = sp.Symbol("x")
expression = input("Enter your function: ")
f = sp.sympify(expression)
n = int(input("Number of terms: "))
a = float(input("Centered at point: "))

def taylor_series(f_prime, a, n):

    i = 0
    taylor = ""

    for i in range(n):
        f_prime = sp.diff(f, x, n)

        f_prime_str = str(f_prime)
        f_prime_evaluated = lambda x: eval(f_prime_str)
        f_prime_of_a = f_prime_evaluated(a)

        term = (f_prime_of_a / math.factorial(i)) * (x - a)**i
        
        taylor += str(term)
    return taylor

taylor_expansion = taylor_series(f, a, n)
print(taylor_expansion)
