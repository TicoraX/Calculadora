import urllib.request
import json
import os
import time

# Caché local para tasas de cambio
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'rates_cache.json')
# TTL en segundos (12 horas)
CACHE_TTL = 12 * 60 * 60


def _load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ts = data.get('timestamp')
        if not ts or (time.time() - ts) > CACHE_TTL:
            return None
        return data.get('rates')
    except Exception:
        return None


def _save_cache(rates):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'timestamp': time.time(), 'rates': rates}, f)
    except Exception:
        pass


def obtener_tasas_monedas():
    """Se conecta a una API pública para obtener tasas de cambio.
    Si la API falla, intenta usar una caché local válida.
    Retorna un diccionario con las tasas referenciadas al Dólar (USD), o None.
    """
    # Intentar obtener desde la API
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            data = json.loads(response.read().decode())
            rates = data.get("rates", {})
            if rates:
                _save_cache(rates)
                return rates
    except Exception:
        # Caída de la API — intentar caché
        cached = _load_cache()
        return cached
    # Fallback a caché si API retorna vacío
    cached = _load_cache()
    return cached

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
