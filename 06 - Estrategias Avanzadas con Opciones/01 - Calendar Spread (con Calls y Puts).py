# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.stats import norm

# Obtener Fechas de Vencimiento
ticker = "SPY"
activo = yf.Ticker(ticker=ticker)
fechas_disponibles = np.array([pd.to_datetime(f) for f in activo.options])

# Fechas objetivos (30 y 60 días)
hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
fecha_30 = hoy + timedelta(days=30)
fecha_60 = hoy + timedelta(days=60)

# Encontrar Vencimientos Aprox.
fecha_1 = fechas_disponibles[np.argmin(np.abs(fechas_disponibles - fecha_30))].strftime("%Y-%m-%d")
fecha_2 = fechas_disponibles[np.argmin(np.abs(fechas_disponibles - fecha_60))].strftime("%Y-%m-%d")

print(f"Fechas Seleccionadas: {fecha_1} | {fecha_2}")

# Obtener Contratos (Cadena de Opciones)
calls1, puts1, underlying_info = activo.option_chain(date=fecha_1)
calls2, puts2, underlying_info = activo.option_chain(date=fecha_2)

# Extraer Datos y Parámetros
precio_actual = underlying_info["regularMarketPrice"]
print("Precio actual:", precio_actual)
precio_ejercicio = int(precio_actual)

# Definición de Estrategias:
#   - Calendar Spread (con Calls): Vender Call (K con vencimiento cercano) + Comprar Call (K con vencimiento lejano)
#   - Calendar Spread (con Puts): Vender Put (K con vencimiento cercano) + Comprar Put (K con vencimiento lejano)

# Contratos
contrato_call_cp = calls1[calls1["strike"] == precio_ejercicio]
contrato_call_lp = calls2[calls2["strike"] == precio_ejercicio]
contrato_put_cp = puts1[puts1["strike"] == precio_ejercicio]
contrato_put_lp = puts2[puts2["strike"] == precio_ejercicio]

# Validar que los contratos existen
if (contrato_call_cp.empty or contrato_call_lp.empty or contrato_put_cp.empty or contrato_put_lp.empty):
    raise ValueError("No se encontraron contratos en al menos uno de los vencimientos para el strike seleccionado")

# Obtener Parámetros
r = 0.01
T_cp = (pd.to_datetime(fecha_1) - hoy).days / 365
T_lp = (pd.to_datetime(fecha_2) - hoy).days / 365
vol_call_cp = contrato_call_cp["impliedVolatility"].iloc[0]
vol_call_lp = contrato_call_lp["impliedVolatility"].iloc[0]
vol_put_cp = contrato_put_cp["impliedVolatility"].iloc[0]
vol_put_lp = contrato_put_lp["impliedVolatility"].iloc[0]

# Rango de Precios al Vencimiento
precios = np.linspace(start=precio_actual * 0.85, stop=precio_actual * 1.15, num=500)

# Función general BS
def opcion_bs(S, K, T, r, sigma, tipo="call"):
    
    """
    Calcula el precio de una opción tipo 'call' o 'put' usando Black-Scholes.
    """
    
    # Primas Teóricas
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if tipo == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
# Calcular/Obtener Primas Call Calendar Spread
prima_corta_call = contrato_call_cp["lastPrice"].iloc[0]
prima_larga_call = contrato_call_lp["lastPrice"].iloc[0]
costo_neto_call = prima_larga_call - prima_corta_call

# Payoff Call Calendar Spread
valor_call_corta = np.maximum(precios - precio_ejercicio, 0)
valor_call_larga = opcion_bs(S=precios, K=precio_ejercicio, T=T_lp - T_cp, r=r, sigma=vol_call_lp, tipo="call")
ganancia_call = valor_call_larga - valor_call_corta - costo_neto_call

# Calcular/Obtener Primas Put Calendar Spread
prima_corta_put = contrato_put_cp["lastPrice"].iloc[0]
prima_larga_put = contrato_put_lp["lastPrice"].iloc[0]
costo_neto_put = prima_larga_put - prima_corta_put

# Payoff Put Calendar Spread
valor_put_corta = np.maximum(precio_ejercicio - precios, 0)
valor_put_larga = opcion_bs(S=precios, K=precio_ejercicio, T=T_lp - T_cp, r=r, sigma=vol_put_lp, tipo="put")
ganancia_put = valor_put_larga - valor_put_corta - costo_neto_put

# Imprimir resumen de primas
print(f"Calls -> Prima Corta: {prima_corta_call:.2f}, Prima Larga: {prima_larga_call:.2f}, Débito Neto: {costo_neto_call:.2f}")
print(f"Puts -> Prima Corta: {prima_corta_put:.2f}, Prima Larga: {prima_larga_put:.2f}, Débito Neto: {costo_neto_put:.2f}")

# Gráficos en Subplots
plt.style.use("dark_background")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

# Subplot 1: Calendar Spread con Calls
ax1.plot(precios, ganancia_call, label="Calendar Call", color="lime", lw=2)
ax1.fill_between(x=precios, y1=ganancia_call, y2=0, where=ganancia_call >= 0, color="green", alpha=0.3)
ax1.fill_between(x=precios, y1=ganancia_call, y2=0, where=ganancia_call < 0, color="red", alpha=0.3)
ax1.axhline(y=0, color="white", lw=1)
ax1.axvline(precio_ejercicio, color="white", lw=1.2, linestyle="--")
ax1.set_title("Calendar Spread con Calls")
ax1.set_xlabel("Precio del Subyacente")
ax1.set_ylabel("Ganancia / Pérdida")
ax1.grid(alpha=0.3)
ax1.legend()

# Subplot 2: Calendar Spread con Puts
ax2.plot(precios, ganancia_put, label="Calendar Put", color="cyan", lw=2)
ax2.fill_between(x=precios, y1=ganancia_put, y2=0, where=ganancia_put >= 0, color="green", alpha=0.3)
ax2.fill_between(x=precios, y1=ganancia_put, y2=0, where=ganancia_put < 0, color="red", alpha=0.3)
ax2.axhline(y=0, color="white", lw=1)
ax2.axvline(precio_ejercicio, color="white", lw=1.2, linestyle="--")
ax2.set_title("Calendar Spread con Puts")
ax2.set_xlabel("Precio del Subyacente")
ax2.set_ylabel("Ganancia / Pérdida")
ax2.grid(alpha=0.3)
ax2.legend()

plt.suptitle("Comparación de Calendar Spread: Calls vs Puts", fontsize=14)
plt.tight_layout()
plt.show()

# Recordatorio:
#   - Los Calendar Spreads combinan la venta de una opción corta y una compra de opción larga con mismo strike pero
#     diferente vencimiento. Se benefician del paso del tiempo y cambios en la volatilidad.
#   - El mayor beneficio ocurre cuando el subyacente permanece cercano al precio de ejercicio al vencimiento de la
#     opción corta, generando un perfil de ganancia tipo campana.
#   - Tiene Delta cercano a cero inicialmente, pero Gamma alta cerca del strike. Eso permite sensibilidad a pequeños
#     movimientos en esa zona si ser direccional.
#   - La posición gana con el paso del tiempo si el precio se mantiene cerca del strike, ya que la opción corta pierde
#     valor más rápido que la larga.
#   - Es sensible positivamente a aumentos en la volatilidad implícita, especialmente porque la opción larga (más lejana)
#     es más afectada que la corta.
