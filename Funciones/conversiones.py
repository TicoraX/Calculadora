import urllib.request
import json

def obtener_tasas_monedas():
    """
    Se conecta a una API pública y gratuita para obtener las tasas de cambio.
    Retorna un diccionario con las tasas referenciadas al Dólar (USD).
    """
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get("rates", {})
    except Exception:
        return None

def convertir_moneda(cantidad, de_moneda, a_moneda, tasas):
    if not tasas or de_moneda not in tasas or a_moneda not in tasas:
        return None
    # Convertimos primero la moneda origen a USD (la base) y luego a la moneda destino
    en_usd = cantidad / tasas[de_moneda]
    resultado = en_usd * tasas[a_moneda]
    return resultado

# ----------------- PESOS -----------------
# Unidad base: Kilos
FACTORES_PESO = {
    "Kilos": 1.0,
    "Libras": 2.20462,
    "Onzas": 35.274,
    "Gramos": 1000.0,
    "Miligramos": 1000000.0
}

def convertir_peso(cantidad, de_peso, a_peso):
    # Convertimos el origen a kilos (base) y luego a la unidad destino
    en_kilos = cantidad / FACTORES_PESO[de_peso]
    return en_kilos * FACTORES_PESO[a_peso]


# ----------------- DISTANCIAS -----------------
# Unidad base: Metros
FACTORES_DISTANCIA = {
    "Metros": 1.0,
    "Kilómetros": 0.001,
    "Millas": 0.000621371,
    "Yardas": 1.09361,
    "Pies": 3.28084,
    "Pulgadas": 39.3701
}

def convertir_distancia(cantidad, de_dist, a_dist):
    # Convertimos el origen a metros (base) y luego a la unidad destino
    en_metros = cantidad / FACTORES_DISTANCIA[de_dist]
    return en_metros * FACTORES_DISTANCIA[a_dist]