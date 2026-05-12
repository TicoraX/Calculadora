import math

# crear funciones para calcular el area y el perimetro de figuras geometricas
# Area del cuadrado: lado * lado
# Perimetro del cuadrado: 4 * lado
# Area del rectangulo: base * altura
# Perimetro del rectangulo: 2 * (base + altura)
# Area del triangulo: (base * altura) / 2
# Perimetro del triangulo: lado1 + lado2 + lado3
# Area del circulo: pi * radio * radio
# Perimetro del circulo: 2 * pi * radio

def area_cuadrado(lado):
    return lado ** 2

def perimetro_cuadrado(lado):
    return lado * 4

def area_rectangulo(base, altura):
    return base * altura

def perimetro_rectangulo(base, altura):
    return 2 * (base + altura)

def area_triangulo(base, altura):
    return (base * altura) / 2

def perimetro_triangulo(lado1, lado2, lado3):
    return lado1 + lado2 + lado3

def area_circulo(radio):
    return math.pi * (radio ** 2)

def perimetro_circulo(radio):
    return 2 * math.pi * radio
