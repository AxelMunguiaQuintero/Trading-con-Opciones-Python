# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from datetime import datetime
import numpy as np
from scipy.stats import norm # pip install scipy

# Definir función que simule el Modelo de Black-Scholes-Merton
def calcular_opcion_bsm(S: float, K: float, T: float, r: float, sigma: float, q: float, tipo: str = "call"):
    
    """
    Calcula el precio teórico de una opción europea usando el modelo de BSM.
    """
    
    # Obtener d1 y d2
    d1 = (np.log(S/K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Calcular la Prima
    if tipo == "call":
        precio = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif tipo == "put":
        precio = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("Tipo de Opción no válido. Usar 'call' o 'put'.")
        
    return precio

# Parámetros
S = 100
K = 100
T = 365/365
r = 0.05
sigma = 0.20
q = 0.02

# Precio del Call
precio_call = calcular_opcion_bsm(S=S, K=K, T=T, r=r, sigma=sigma, q=q, tipo="call")
print(f"Precio de la Opción Call: {precio_call:.2f}")

# Precio del Put
precio_put = calcular_opcion_bsm(S=S, K=K, T=T, r=r, sigma=sigma, q=q, tipo="put")
print(f"Precio de la Opción Put: {precio_put:.2f}")

# Comprobarlo con Datos Reales
ticker = "TSLA"
stock = yf.Ticker(ticker=ticker)

# Precio Actual
precio_actual = round(stock.history(period="1d")["Close"].iloc[0], 4)
print(f"Precio Actual del Activo: {ticker} -> {precio_actual:.4f}")

# Obtener Fechas Disponibles (Seleccionar una)
fechas_disponibles = stock.options
fecha_objetivo = fechas_disponibles[5]

# Extraer Cadena de Opciones
calls, puts, _ = stock.option_chain(date=fecha_objetivo)
# Seleccionar Strike (Cercano al precio actual)
indice_df = abs(calls["strike"] - precio_actual).argmin()
strike_indice = calls["strike"].iloc[indice_df]
print("Precio de Ejercicio Seleccionado:", strike_indice)

# Seleccionar el Call y Put con el mismo Strike
try:
    call_seleccionado = calls[calls["strike"] == strike_indice]
    put_seleccionado = puts[puts["strike"] == strike_indice]
    
    # Calcular el tiempo restante hasta el vencimiento
    fecha_hoy = datetime.now()
    fecha_vencimiento = datetime.strptime(fecha_objetivo, "%Y-%m-%d")
    T_real = ((fecha_vencimiento - fecha_hoy).days) / 365
    
    # Obtener Volatilidades Implícitas (Volatilidad Esperada en el Futuro)
    call_volatility = call_seleccionado["impliedVolatility"].iloc[0]
    put_volatility = put_seleccionado["impliedVolatility"].iloc[0]
    
    # Suponer que no hay dividendos (Tesla no paga dividendos)
    q = 0.0
    
    # Tasa libre de riesgo (bonos 3 meses)
    r = yf.Ticker(ticker="^IRX").history(period="1d")["Close"].iloc[-1] / 100
    
    # Calcular la Prima
    prima_call = calcular_opcion_bsm(S=precio_actual, K=call_seleccionado["strike"].iloc[0], T=T_real, 
                                     r=r, sigma=call_volatility, q=q, tipo="call")
    prima_put = calcular_opcion_bsm(S=precio_actual, K=put_seleccionado["strike"].iloc[0], T=T_real, 
                                     r=r, sigma=put_volatility, q=q, tipo="put")
    
    # Desplegar Datos Generales
    print(f"Contrato -> Activo: {ticker} | Strike: {call_seleccionado['strike'].iloc[0]} | Vencimiento: {fecha_vencimiento}")

    # Revisar Call
    print(f"Prima Calculada con el Modelo de BSM (call) para {ticker}: {prima_call:.4f}")
    print(f"Precio Real de la Prima (Call): {call_seleccionado['lastPrice'].iloc[0]:.4f}\n")
    
    # Revisar Put
    print(f"Prima Calculada con el Modelo de BSM (put) para {ticker}: {prima_put:.4f}")
    print(f"Precio Real de la Prima (Put): {put_seleccionado['lastPrice'].iloc[0]:.4f}\n")
    
except:
    print("No hay un contrato disponible con el mismo strike para los puts...")

# Recordatorio:
#   - El Modelo BSM calcula el precio teórico de opciones europeas usando variables como precio actual, strike,
#     volatilidad, tiempo y tasa libre de riesgo para valorar contratos de opciones.
#   - El Modelo asume que los precios del activo subyacente siguen un movimiento lognormal, con rendimientos
#     distribuidos normalmente, lo que permite usar probabilidades para estimar el valor esperado de la opción
#     al vencimiento.
