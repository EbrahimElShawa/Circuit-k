from sympy import symbols, sympify


def evaluate_equation_for_range(equation, t_vec):
    t = symbols('t')

    expr = sympify(equation)
    source = []
    for value in t_vec:
        source.append(expr.subs(t, value).evalf())
        print(f"value of {value} second is {source[-1]}")
    return source


class NooValidExpression(Exception):
    def __init__(self, message="The equation is not valid."):
        self.message = message
        super().__init__(self.message)
