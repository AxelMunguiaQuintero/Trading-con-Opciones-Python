# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import minimize_scalar 
from datetime import datetime

# Descargar Cadena de Opciones
ticker = "TSLA"
ticker_instancia = yf.Ticker(ticker=ticker)
fechas_disponibles = ticker_instancia.options

# Definir fecha objetivo
fecha_objetivo = fechas_disponibles[5]
cadena_opciones = ticker_instancia.option_chain(date=fecha_objetivo)
calls, puts, underlying_price = cadena_opciones

# Seleccionar un Contrato
print("Precio Actual del Activo:", underlying_price["regularMarketPrice"])
contrato_strike = 325 # Ajustar según el precio de mercado

contrato_call = calls[calls["strike"] == contrato_strike]
print(contrato_call.T)

# Definir Tasa Libre de Riesgo
tasa_libre_riesgo = 0.05

# Calcular el tiempo hasta el vencimiento en años
fecha_vencimiento = pd.to_datetime(fecha_objetivo)
fecha_actual = datetime.now()
tiempo_a_vencimiento = (fecha_vencimiento - fecha_actual).days / 365
print(f"Tiempo hasta el vencimiento (en años): {tiempo_a_vencimiento:.4f} años")

# Función BSM
def precio_opcion(S, K, T, r, sigma, q = 0, tipo = "call"):
    
    """
    Calcula el precio de una opción utilizando el Modelo de Black-Scholes-Merton.
    """
    
    # Obtener valores auxiliares
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Calcular la Prima de la Opción
    if tipo == "call":
        precio = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        precio = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        
    return precio

# Probar Función
prima_call = precio_opcion(S=underlying_price["regularMarketPrice"], K=contrato_call["strike"].iloc[0], 
                           T=tiempo_a_vencimiento, r=tasa_libre_riesgo, sigma=contrato_call["impliedVolatility"].iloc[0],
                           tipo="call")
print("Precio de la Opción Teóricamente:", prima_call)
print("Precio Real:", contrato_call["lastPrice"].iloc[0])
    
# Encontrar Volatilidad Implícita (Como si no se conociera)
def volatilidad_implicita(precio_opcion_mercado, S, K, T, r, q=0, tipo="call"):
    
    """
    Encuentra la volatilidad implícita que iguala el precio teórico con el de mercado usando
    minimización de error absoluto.
    """
    
    # Función Objetivo: Diferencia absoluta entre precios
    def error(sigma): 
        precio_teorico = precio_opcion(S, K, T, r, sigma, q, tipo)
        return abs(precio_teorico - precio_opcion_mercado)
    
    # Búsqueda de la volatilidad. Definir un rango de valores, entre 0.1% y 500%
    resultado = minimize_scalar(fun=error, bounds=(0.001,5), method="bounded")
    
    # Validar que la optimización fue exitosa
    if resultado.success:
        return resultado.x
    else:
        return np.nan

# Optimizar
precio_opcion_call = contrato_call["lastPrice"].iloc[0]
strike = contrato_call["strike"].iloc[0]
vol_impl = volatilidad_implicita(precio_opcion_mercado=precio_opcion_call, S=underlying_price["regularMarketPrice"],
                                 K=strike, T=tiempo_a_vencimiento, r=tasa_libre_riesgo)

print(f"Volatilidad Implícita calculada para el contrato Call con strike {strike}: {vol_impl * 100:.4f}%")
print(f"Volatilidad Implícita Real: {contrato_call['impliedVolatility'].iloc[0] * 100:.4f}%")

# Recordatorio:
#   - La Volatilidad Implícita representa la expectativa futura del mercado sobre la variabilidad del precio de un activo.
#     Se extrae del precio actual de las opciones y refleja la percepción del riesgo y la incertidumbre esperada de los inversores.
