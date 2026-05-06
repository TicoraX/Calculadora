# Funciones simples para el manejo del apartado de la calculadora simple de dos digitos.

def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    #No se puede dividir entre 0 dah
    if b != 0:
        return a / b
    else:
        return "Error: División por cero no permitida"

def raiz_cuadrada(a):
    #devolvemos la raíz cuadrada de un número, si el número es negativo, devolvemos un mensaje de error
    if a >= 0:
        return a ** 0.5
    else:
        return "Error: No se puede calcular la raíz cuadrada de un número negativo"    

def porcentaje(base, valor, operacion=None):
    # Trabajamos el porcentaje como una calculadora: el numero anterior es la base.
    resultado_porcentaje = base * valor / 100

    if operacion is None:
        return resultado_porcentaje

    if operacion == "+":
        return suma(base, resultado_porcentaje)
    elif operacion == "-":
        return resta(base, resultado_porcentaje)
    elif operacion == "*":
        return multiplicacion(base, resultado_porcentaje)
    elif operacion == "/":
        return division(base, resultado_porcentaje)

    return "Error: Operacion no valida"
    
