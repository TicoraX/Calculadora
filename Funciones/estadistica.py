import statistics
import re

def calcular_estadistica(datos_str):
    """
    Toma una cadena de números en cualquier formato (comas, espacios, corchetes)
    y devuelve un diccionario con los cálculos estadísticos.
    """
    try:
        # Extrae automáticamente todos los números (positivos, negativos, con o sin decimales)
        # Esto permite al usuario pegar formatos como "[1.5; -2; 3]" o "Valores: 1, 2, 3" sin que falle.
        numeros_str = re.findall(r'[-+]?\d*\.?\d+', datos_str)
        datos = [float(x) for x in numeros_str]
        
        if not datos:
            return None
            
        res = {
            "Media (Promedio)": statistics.mean(datos),
            "Mediana": statistics.median(datos),
            "Mínimo": min(datos),
            "Máximo": max(datos),
            "Suma Total": sum(datos),
            "Total Elementos": len(datos)
        }
        
        try:
            res["Moda"] = statistics.mode(datos)
        except statistics.StatisticsError:
            res["Moda"] = "Varias/Ninguna"
            
        if len(datos) > 1:
            res["Varianza"] = statistics.variance(datos)
            res["Desviación Est."] = statistics.stdev(datos)
        else:
            res["Varianza"] = 0
            res["Desviación Est."] = 0
            
        return res
    except Exception:
        return None
