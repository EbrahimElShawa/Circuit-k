from Circuits import Circuit
import matplotlib.pyplot as plt
import circuitTools
from create_files import create
import pandas as pd
from sympy import symbols, sympify


if __name__ == '__main__':
    # cir = Circuit("assets/net/net.txt")
    # circuitTools.picture(cir)
    # circuitTools.plot_branch(cir, 2, 1, 2, -1, -1)
    # circuitTools.excel(cir)
    # circuitTools.picture("assets/net/net.txt")
    # circuitTools.plot_branch(cir,1, 1, -1, 0, 2)
    t = symbols('t')
    equation = input("Enter your equation: ")
    expr = sympify(equation)
    source = []
    print(equation)
    for value in range(20):
        result = expr.subs(t, value).evalf()
        print(f"value of {value} second is {result}")

