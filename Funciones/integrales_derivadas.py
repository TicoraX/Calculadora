import sympy as sp

def calcular_derivada(expresion_str, variable='x'):
    try:
        x = sp.Symbol(variable)
        expresion_str = expresion_str.replace('^', '**')
        expr = sp.sympify(expresion_str)
        derivada = sp.diff(expr, x)
        return str(derivada).replace('**', '^')
    except Exception:
        return None

def calcular_integral_indefinida(expresion_str, variable='x'):
    try:
        x = sp.Symbol(variable)
        expresion_str = expresion_str.replace('^', '**')
        expr = sp.sympify(expresion_str)
        integral = sp.integrate(expr, x)
        return str(integral).replace('**', '^') + " + C"
    except Exception:
        return None

def calcular_integral_definida(expresion_str, a, b, variable='x'):
    try:
        x = sp.Symbol(variable)
        expresion_str = expresion_str.replace('^', '**')
        expr = sp.sympify(expresion_str)
        integral = sp.integrate(expr, (x, float(a), float(b)))
        # Si el resultado es un número, evaluarlo
        if integral.is_number:
            return f"{float(integral.evalf()):,.4f}"
        return str(integral).replace('**', '^')
    except Exception:
        return None
