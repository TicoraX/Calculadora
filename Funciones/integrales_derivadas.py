import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Transformaciones avanzadas para entender notación humana (ej: 2x -> 2*x, x(x+1) -> x*(x+1))
transformations = (standard_transformations + (implicit_multiplication_application,))

def parsear_y_limpiar(expresion_str):
    # Traducir sintaxis común
    expresion_str = expresion_str.replace('^', '**')
    expresion_str = expresion_str.replace('sen', 'sin')
    expresion_str = expresion_str.replace('ln', 'log')
    # sympy parsea inteligentemente
    return parse_expr(expresion_str, transformations=transformations)

def calcular_derivada(expresion_str, variable='x'):
    try:
        x = sp.Symbol(variable)
        expr = parsear_y_limpiar(expresion_str)
        derivada = sp.diff(expr, x)
        return str(derivada).replace('**', '^')
    except Exception:
        return None

def calcular_integral_indefinida(expresion_str, variable='x'):
    try:
        x = sp.Symbol(variable)
        expr = parsear_y_limpiar(expresion_str)
        integral = sp.integrate(expr, x)
        return str(integral).replace('**', '^') + " + C"
    except Exception:
        return None

def calcular_integral_definida(expresion_str, a, b, variable='x'):
    try:
        x = sp.Symbol(variable)
        expr = parsear_y_limpiar(expresion_str)
        integral = sp.integrate(expr, (x, float(a), float(b)))
        # Si el resultado es un número, evaluarlo a decimal
        if integral.is_number:
            return f"{float(integral.evalf()):,.4f}"
        return str(integral).replace('**', '^')
    except Exception:
        return None
