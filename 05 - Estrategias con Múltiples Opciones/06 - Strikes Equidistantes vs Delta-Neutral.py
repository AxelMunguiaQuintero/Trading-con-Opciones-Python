# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import norm
import matplotlib.pyplot as plt

# Definir Modelo BS
def bs_precio(S, K, T, r, sigma, tipo="call"):
    
    """
    Calcula el precio de una opción con el modelo de BS
    """
    
    # Calcular Prima
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    prima = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2) if tipo == "call" else \
        K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
    return prima

# Parámetros del Iron Condor
K1, K2, K3, K4 = 80, 90, 110, 120 # Strikes: put buy, put sell, call sell, call buy
S = 100
T = 1
sigma = 0.30
r = 0.05
# Rango de Precios al Vencimiento
S_Vencimiento = np.linspace(start=50, stop=150, num=500)

# Calcular Primas
P1 = bs_precio(S=S, K=K1, T=T, r=r, sigma=sigma, tipo="put") # Put Compra
P2 = bs_precio(S=S, K=K2, T=T, r=r, sigma=sigma, tipo="put") # Put Venta
C2 = bs_precio(S=S, K=K3, T=T, r=r, sigma=sigma, tipo="call") # Call Venta
C1 = bs_precio(S=S, K=K4, T=T, r=r, sigma=sigma, tipo="call") # Call Compra
prima_neta = (P2 - P1) + (C2 - C1) # Ingreso Neto (Crédito)

# Diagrama de Pago
payoff = prima_neta - np.maximum(K2 - S_Vencimiento, 0) + np.maximum(K1 - S_Vencimiento, 0) - \
    np.maximum(S_Vencimiento - K3, 0) + np.maximum(S_Vencimiento - K4, 0)
    
# Generar línea del valor de nuestra posición (rendimiento) para los distintos niveles de precios
payoff_array = (bs_precio(S=S_Vencimiento, K=K1, T=T, r=r, sigma=sigma, tipo="put")) * 1 + \
    (bs_precio(S=S_Vencimiento, K=K2, T=T, r=r, sigma=sigma, tipo="put")) * -1 + \
    (bs_precio(S=S_Vencimiento, K=K4, T=T, r=r, sigma=sigma, tipo="call")) * 1 + \
    (bs_precio(S=S_Vencimiento, K=K3, T=T, r=r, sigma=sigma, tipo="call")) * -1 + prima_neta
    
# Generar Plot de Estrategia
plt.figure(figsize=(18, 6), dpi=300)
plt.plot(S_Vencimiento, payoff, color="orange", lw=4, label="Diagrama de Pago al Vencimiento")
plt.plot(S_Vencimiento, payoff_array, color="blue", lw=2, label="Beneficio Actual")
# Agregar líneas de strikes y ejes
colores = ["blue", "pink", "black", "green"]
for n, k in enumerate([K1, K2, K3, K4]):
    plt.axvline(x=k, linestyle="--", label=f"Strike K{n+1}", color=colores[n], lw=2)
plt.axhline(y=0, color="black", linestyle="--", lw=0.5)

# Añadir Etiquetas y Título
plt.title("Iron Condor", fontweight="bold")
plt.xlabel("Precio del Subyacente", fontsize=9)
plt.ylabel("B/P", fontsize=9)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Iron Condor con Datos Reales:
    
# Descargar Datos
ticker = "SPY"
ticker_instancia = yf.Ticker(ticker=ticker)
fecha_objetivo = ticker_instancia.options[3]
# Obtener Cadena de Opciones
calls, puts, underlying_info = ticker_instancia.option_chain(date=fecha_objetivo)
# Precio Actual del Activo
precio_actual = underlying_info["regularMarketPrice"]

# Definir strikes
K1 = int(precio_actual - 9) # Put Comprada
K2 = int(precio_actual - 4) # Put Vendida
K3 = int(precio_actual + 7) # Call Vendida
K4 = int(precio_actual + 12) # Call Comprada

# Buscar Primas en la Cadena de Opciones
def buscar_prima(strike, tipo="call"):
    
    """
    Función que encuentra el contrato con el strike específicado y devuelve la prima
    """
    
    df = calls if tipo == "call" else puts
    fila = df[df["strike"] == strike]
    if fila.empty:
        return np.nan
    return fila["lastPrice"].iloc[0]

# Obtener Primas
P1 = buscar_prima(strike=K1, tipo="put") # Put Comprado
P2 = buscar_prima(strike=K2, tipo="put") # Put Vendido
C2 = buscar_prima(strike=K3, tipo="call") # Call Vendido
C1 = buscar_prima(strike=K4, tipo="call") # Call Comprado
prima_neta = (P2 - P1) + (C2 - C1)

# Rango de Precios
S_Vencimiento = np.linspace(start=precio_actual - 50, stop=precio_actual + 50, num=500)
payoff = prima_neta - np.maximum(K2 - S_Vencimiento, 0) + np.maximum(K1 - S_Vencimiento, 0) - \
    np.maximum(S_Vencimiento - K3, 0) + np.maximum(S_Vencimiento - K4, 0)
    
# Beneficio Actual
T_restante = (pd.to_datetime(fecha_objetivo) - datetime.now()).days / 365
payoff_array = (bs_precio(S=S_Vencimiento, K=K1, T=T_restante, r=r, 
                          sigma=puts[puts["strike"] == K1]["impliedVolatility"].iloc[0], tipo="put") * 1) + \
    (bs_precio(S=S_Vencimiento, K=K2, T=T_restante, r=r, 
                              sigma=puts[puts["strike"] == K2]["impliedVolatility"].iloc[0], tipo="put") * -1) + \
    (bs_precio(S=S_Vencimiento, K=K4, T=T_restante, r=r, 
                              sigma=calls[calls["strike"] == K4]["impliedVolatility"].iloc[0], tipo="call") * 1) + \
    (bs_precio(S=S_Vencimiento, K=K3, T=T_restante, r=r, 
                              sigma=calls[calls["strike"] == K3]["impliedVolatility"].iloc[0], tipo="call") * -1) + prima_neta

# Generar Plot de Estrategia
plt.figure(figsize=(18, 6), dpi=300)
plt.plot(S_Vencimiento, payoff, color="orange", lw=4, label="Diagrama de Pago al Vencimiento")
plt.plot(S_Vencimiento, payoff_array, color="blue", lw=2, label="Beneficio Actual")
# Agregar líneas de strikes y ejes
colores = ["blue", "pink", "black", "green"]
for n, k in enumerate([K1, K2, K3, K4]):
    plt.axvline(x=k, linestyle="--", label=f"Strike K{n+1}", color=colores[n], lw=2)
plt.axhline(y=0, color="black", linestyle="--", lw=0.5)
plt.axvline(precio_actual, linestyle=":", label=f"Precio Actual: {precio_actual:.2f}")

# Máxima Pérdida de Cada Lado
lado_izquierdo = np.min(payoff[S_Vencimiento <= precio_actual])
lado_derecho = np.min(payoff[S_Vencimiento >= precio_actual])

plt.annotate(text=f"Máxima Pérdida ${lado_izquierdo:.4f}", xy=(580, lado_izquierdo), xytext=(565, lado_izquierdo + 1),
             arrowprops=dict(arrowstyle="->"), fontsize=12)
plt.annotate(text=f"Máxima Pérdida ${lado_derecho:.4f}", xy=(630, lado_derecho), xytext=(635, lado_derecho + 1),
             arrowprops=dict(arrowstyle="->"), fontsize=12)

# Añadir Etiquetas y Título
plt.title("Iron Condor", fontweight="bold")
plt.xlabel("Precio del Subyacente", fontsize=9)
plt.ylabel("B/P", fontsize=9)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Recordatorio:
#   - La asimetría en los strikes puede provocar que el delta total de la posición no sea cero ni esté balanceado,
#     generando una exposición direccional no intencionada que puede hacer que la estrategia se más sensible
#     a movimientos del precio en una dirección específica.
