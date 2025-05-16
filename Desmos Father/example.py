import sympy
from sympy import *

def taylor_series(function, variable, at_point, n):

    i = 0
    taylor = 0
    while i <= n:
        p = (function.diff(variable, i).subs(variable, at_point) / factorial(i)) * (variable - at_point)**i
        taylor += p
        i += 1
    return taylor

x = symbols('x')
function = sin(x) 
at_point = 0      
n = 4             

taylor_expansion = taylor_series(function, x, at_point, n)
print(taylor_expansion)