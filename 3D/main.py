import sympy as sp
import numpy as np
import math

x = sp.Symbol("x")
expression = input("Enter your function: ")
f = sp.sympify(expression)
n = int(input("Order of differentiating: "))
a = float(input("Differentiate at point: "))

f_prime = sp.diff(f, x, n)

f_prime_str = str(f_prime)
f_prime_evaluated = lambda x: eval(f_prime_str)
f_prime_of_a = f_prime_evaluated(a)

print("Original function: ",expression)
print(f"Derivative of order {n}: ",f_prime)
print(f"Derivative at point {a}: ", f_prime_of_a)