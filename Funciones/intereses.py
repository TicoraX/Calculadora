# Funciones de intereses simples.
def interes_simple(Capital_Inicial, Interes, Tiempo):
    # Formula de interes simple: I = P * r * t
    return Capital_Inicial * Interes * Tiempo

# Ahora crearemos la funcion de interes compuesto.
def interes_compuesto(Capital_Inicial, Interes, Tiempo):
    # Formula de interes compuesto: I = P * (1 + r)^t
    return Capital_Inicial * (1 + Interes) ** Tiempo
