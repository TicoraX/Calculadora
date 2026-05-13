import statistics

def calcular_estadistica(datos_str):
    """
    Toma una cadena de números separados por comas o espacios,
    y devuelve un diccionario con los cálculos estadísticos.
    """
    try:
        datos = [float(x.strip()) for x in datos_str.replace(',', ' ').split() if x.strip()]
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
