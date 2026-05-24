import math
from Funciones.cientifica import seno, coseno, tangente, logaritmo_base10, logaritmo_Natural, factorial
from Funciones.simples import raiz_cuadrada
import re

def test_eval():
    exps = ["sin(90)", "e^2", "tan(45)+e", "log(10)", "π*2", "√(9)"]
    contexto = {
        'seno': seno,
        'coseno': coseno,
        'tangente': tangente,
        'logaritmo_base10': logaritmo_base10,
        'logaritmo_Natural': logaritmo_Natural,
        'factorial': factorial,
        'raiz_cuadrada': raiz_cuadrada,
        'math': math,
        '__builtins__': __builtins__
    }
    
    for exp_orig in exps:
        exp = exp_orig
        exp = exp.replace('π', 'math.pi')
        exp = re.sub(r'\be\b', 'math.e', exp)
        exp = re.sub(r'\bsin\b', 'seno', exp)
        exp = re.sub(r'\bcos\b', 'coseno', exp)
        exp = re.sub(r'\btan\b', 'tangente', exp)
        exp = re.sub(r'\blog\b', 'logaritmo_base10', exp)
        exp = re.sub(r'\bln\b', 'logaritmo_Natural', exp)
        exp = exp.replace('^', '**')
        exp = exp.replace('√', 'raiz_cuadrada')
        try:
            res = str(eval(exp, {"__builtins__": __builtins__}, contexto))
            print(f"{exp_orig} -> {exp} -> {res}")
        except Exception as e:
            print(f"Error on {exp_orig} ({exp}):", e)

test_eval()
