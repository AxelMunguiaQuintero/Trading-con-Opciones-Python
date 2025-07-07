# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Parámetros generales
precio_actual = 100
T = 1
r = 0.05
sigma = 0.30

# Rangos de Precios al Vencimiento
precios = np.linspace(start=60, stop=140, num=500)

# Función Black-Scholes
def Black_Scholes(S, K, T, r, sigma, tipo="call"):
    
    """
    Función para calcular la prima teórica de una opción.
    """
    
    # Calcular d1 y d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # Obtener Precios
    if tipo == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return  K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
# Definir 1er Posición:
# Call Ratio Spread: Comprar Call ATM (K1) + Vender 2 Calls OTM (K2) con K1 < K2 -> Se recibe un crédito generalmente

# Definir Strikes y Calcular Primas (Call Ratio Spread)
K1_call = 100 # Para Comprar Call
K2_call = 105 # Para vender Calls
prima_long_call = Black_Scholes(S=precio_actual, K=K1_call, T=T, r=r, sigma=sigma, tipo="call")
prima_short_call = Black_Scholes(S=precio_actual, K=K2_call, T=T, r=r, sigma=sigma, tipo="call")

# Prima Neta
net_call_premium = -prima_long_call + 2 * prima_short_call

# Payoff: Diagrama de Pago
payoff_call = (
    
    np.maximum(precios - K1_call, 0) - prima_long_call
    + 2 * (prima_short_call - np.maximum(precios - K2_call, 0))
    
    )

# Break-even - Punto de Equilibrio
be_call_ratio = K2_call + np.max(payoff_call)

# Definir 2da Posición:
# Put Ratio Spread: Comprar Put ATM (K1) + Vender 2 Puts OTM (K2) con K1 > K2 -> Se recibe un crédito generalmente

# Definir Strikes y Calcular Primas (Put Ratio Spread)
K1_put = 100
K2_put = 95
prima_long_put = Black_Scholes(S=precio_actual, K=K1_put, T=T, r=r, sigma=sigma, tipo="put")
prima_short_put = Black_Scholes(S=precio_actual, K=K2_put, T=T, r=r, sigma=sigma, tipo="put")

# Prima Neta
net_put_premium = -prima_long_put + 2 * prima_short_put

# Payoff: Diagrama de Pago
payoff_put = (
    
    np.maximum(K1_put - precios, 0) - prima_long_put
    + 2 * (prima_short_put - np.maximum(K2_put - precios, 0))
    
    )

# Break-even - Punto de Equilibrio
be_put_ratio = K2_put - np.max(payoff_put)

# Gráfico
fig, axs = plt.subplots(2, 1, figsize=(22, 12), dpi=300)

# Plot 1: Call Ratio Spread
axs[0].plot(precios, payoff_call, label="Call Ratio Spread", lw=2, color="blue")
axs[0].fill_between(x=precios, y1=payoff_call, y2=0, where=(payoff_call >= 0), color="green", alpha=0.3)
axs[0].fill_between(x=precios, y1=payoff_call, y2=0, where=(payoff_call < 0), color="red", alpha=0.3)
axs[0].axhline(y=0, color="black", linestyle="--", lw=2)
axs[0].axvline(x=precio_actual, linestyle="--", color="gray", label="Precio Actual", lw=2)

# Break-even y beneficio máximo
axs[0].axvline(x=be_call_ratio, linestyle="--", color="orange", label=f"BE: {be_call_ratio:.2f}", lw=2)
axs[0].plot(K2_call, np.max(payoff_call), "go", label="Ganancia Máxima")
axs[0].annotate(f"Ganancia máx\n${np.max(payoff_call):.2f}", xy=(K2_call, np.max(payoff_call)), 
                xytext=(K2_call + 3, np.max(payoff_call) - 2), 
                arrowprops=dict(arrowstyle="->", color="green"), fontsize=11)

axs[0].set_title(f"Call Ratio Spread: +1 Call {K1_call}, -2 Calls {K2_call}")
axs[0].set_ylabel("Ganancia / Pérdida")
axs[0].legend()
axs[0].grid(True, alpha=0.3)

# Plot 2: Put Ratio Spread
axs[1].plot(precios, payoff_put, label="Put Ratio Spread", lw=2, color="blue")
axs[1].fill_between(x=precios, y1=payoff_put, y2=0, where=(payoff_put >= 0), color="green", alpha=0.3)
axs[1].fill_between(x=precios, y1=payoff_put, y2=0, where=(payoff_put < 0), color="red", alpha=0.3)
axs[1].axhline(y=0, color="black", linestyle="--", lw=2)
axs[1].axvline(x=precio_actual, linestyle="--", color="gray", label="Precio Actual", lw=2)

# Break-even y beneficio máximo
axs[1].axvline(x=be_put_ratio, linestyle="--", color="orange", label=f"BE: {be_put_ratio:.2f}", lw=2)
axs[1].plot(K2_put, np.max(payoff_put), "go", label="Ganancia Máxima")
axs[1].annotate(f"Ganancia máx\n${np.max(payoff_put):.2f}", xy=(K2_put, np.max(payoff_put)), 
                xytext=(K2_put + 3, np.max(payoff_put) - 2), 
                arrowprops=dict(arrowstyle="->", color="green"), fontsize=11)

axs[1].set_title(f"Put Ratio Spread: +1 Put {K1_put}, -2 Puts {K2_put}")
axs[1].set_ylabel("Ganancia / Pérdida")
axs[1].legend()
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Recordatorio:
    
# Tabla Descriptiva para Call Ratio Spread y Put Ratio Spread
tabla_ratio_spread = pd.DataFrame({
    
    "Estrategia": ["Call Ratio Spread", "Put Ratio Spread"],
    "Dirección Esperada": ["Moderadamente Alcista", "Moderadamente Bajista"],
    "Tipo": ["Crédito", "Crédito"],
    "Máx Ganancia": ["Limitada"] * 2,
    "Máx Pérdida": ["Ilimitada (si sube mucho)", "Ilimitada (si baja mucho)"],
    "Posiciones": [
        
        "Comprar 1 Call ATM (K1) + Vender 2 Calls OTM (K2) | K1 < K2",
        "Comprar 1 Put ATM (K1) + Vender 2 Puts OTM (K2) | K1 > K2"
        
        ],
    "Puntos de Equilibrio": [
        
        "K2 + ganancia máxima",
        "K2 - ganancia máxima"
        
        ]
    
    })

print(tabla_ratio_spread)
