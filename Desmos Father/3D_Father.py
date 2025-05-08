from scipy import differentiate
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.symbols("x")
function = input("Enter: ")

try: 
    y = sp.sympify(function)
    dfdx = sp.diff(y, x)
    
    print(dfdx)
except ValueError:
    print("error")
