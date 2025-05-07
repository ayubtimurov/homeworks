from scipy.integrate import dblquad
from sympy import Symbol, integrate

x = Symbol("x")
y = Symbol("y")
function = input(": ")

volume = dblquad(lambda x, y: function, 0, 1, 0, 1)

print(volume)
