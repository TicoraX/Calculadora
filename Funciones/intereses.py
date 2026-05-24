# Funciones de intereses simples.
def interes_simple(Capital_Inicial, Interes, Tiempo):
    # Formula de interes simple: I = P * r * t
    return Capital_Inicial * Interes * Tiempo

# Ahora crearemos la funcion de interes compuesto.
def interes_compuesto(Capital_Inicial, Interes, Tiempo, frecuencia=1):
    """
    Calcula el monto total con interés compuesto.
    - Capital_Inicial: P
    - Interes: tasa anual en decimal (ej: 0.05)
    - Tiempo: tiempo en años
    - frecuencia: número de capitalizaciones por año (n)
    Retorna el monto total (no la ganancia).
    """
    if frecuencia <= 0:
        frecuencia = 1
    n = frecuencia
    return Capital_Inicial * (1 + Interes / n) ** (n * Tiempo)
