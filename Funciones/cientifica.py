import math

# En este apartado de funciones implementaremos las que falta para que una calculadora sea "cientifica", por lo tanto, usaremos la librería math.
# antes cabe mencionar que ahora se podran usar mas operandos, como 3 o mas y se podra usar parentesis, por lo tanto, se usara un enfoque diferente para el manejo de las operaciones.}
# Se implementaran funciones trigonometricas, logaritmos, raices, potencias, etc.

# Ahora crearemos una funcion para poder usarlas.

def calcular(operacion):
    # Implementamos un control de errores para evitar que la funcion eval() lance un error.
    try:
        return eval(operacion)
    except ZeroDivisionError:
        return "Error: División por cero no permitida"
    except Exception as e:
        return f"Error: {e}"

# Implementacion de funciones trigonometricas.

def seno(angulo):
    # Convertimos el angulo a radianes
    rad = math.radians(angulo)
    # Redondeamos a 10 decimales para evitar problemas de precisión (ej: que sin(180) no dé 0 exacto)
    return round(math.sin(rad), 10)

def coseno(angulo):
    # Convertimos el angulo a radianes
    rad = math.radians(angulo)
    return round(math.cos(rad), 10)

def tangente(angulo):
    # La tangente de 90 o 270 (y sus múltiplos) está indefinida, esto previene números gigantes
    if angulo % 180 == 90:
        return "Error: Tangente indefinida (división por cero)"
    rad = math.radians(angulo)
    return round(math.tan(rad), 10)



# Implementacion de funciones trigonometricas inversas.

def seno_inverso(valor):
    # Las funciones inversas reciben un valor entre -1 y 1 (no un ángulo)
    if valor < -1 or valor > 1:
        return "Error: Dominio matemático"
    # math.asin devuelve radianes, así que convertimos el RESULTADO a grados para la calculadora
    return math.degrees(math.asin(valor))

def coseno_inverso(valor):
    if valor < -1 or valor > 1:
        return "Error: Dominio matemático"
    return math.degrees(math.acos(valor))

def tangente_inversa(valor):
    # La tangente inversa acepta cualquier valor
    return math.degrees(math.atan(valor))


# Funciones logaritmicas.

def logaritmo(valor, base):
    # Un logaritmo general donde puedes especificar la base.
    if valor <= 0 or base <= 0 or base == 1:
        return "Error: Dominio matemático"
    return math.log(valor, base)

def logaritmo_base10(valor):
    # Los logaritmos reciben un número, no un ángulo. No hay que convertir a radianes.
    if valor <= 0:
        return "Error: Dominio matemático"
    return math.log10(valor)

def logaritmo_Natural(valor):
    # Logaritmo natural (ln) usando base 'e'
    if valor <= 0:
        return "Error: Dominio matemático"
    return math.log(valor)    

# Otras funciones cientificas (Potencias, Raices, Factorial, etc.)

def factorial(n):
    # El factorial solo aplica a enteros positivos o cero
    if n < 0 or (not isinstance(n, int) and not n.is_integer()):
        return "Error: Dominio matemático (Solo enteros positivos)"
    return math.factorial(int(n))

def potencia(base, exponente):
    return math.pow(base, exponente)

def exponencial(exponente):
    # Calculo de e^x
    return math.exp(exponente)

def raiz_enesima(valor, n):
    if n == 0:
        return "Error: Índice de raíz no puede ser cero"
    if valor < 0 and n % 2 == 0:
         return "Error: Raíz par de número negativo"
    # Usamos potencia fraccionaria para sacar la raíz
    return valor ** (1/n)

def absoluto(valor):
    return math.fabs(valor)

def permutacion(n, k):
    # nPr
    if n < 0 or k < 0 or k > n:
        return "Error: Dominio matemático"
    return math.perm(int(n), int(k))

def combinacion(n, k):
    # nCr
    if n < 0 or k < 0 or k > n:
        return "Error: Dominio matemático"
    return math.comb(int(n), int(k))