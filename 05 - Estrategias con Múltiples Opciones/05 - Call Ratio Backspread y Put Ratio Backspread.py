# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Función BS
def Black_Scholes(S, K, T, r, sigma, option_type):
    
    """
    Modelo de Black-Scholes.
    """
    
    # Realizar Cálculo
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2) if option_type == "call" else \
        K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
# Parámetros del Activo Subyacente
S = 100
T = 91 / 365
r = 0.05
sigma = 0.25

# Rango de Precios del Subyacente
prices = np.linspace(start=S * 0.5, stop=S * 1.5, num=500)

# Call Ratio Backspread (Ratio 1:2): Vender Call (K1) + Comprar 2 Calls (K2) con K1 < K2 -> Débito/Crédito

# Definir Strikes
call_K1 = 95 # Venta del Call
call_K2 = 105 # Compra del Call
call_ratio = 2 # Ratio 1:2

# Cálculo de las Primas
call_prima1 = Black_Scholes(S=S, K=call_K1, T=T, r=r, sigma=sigma, option_type="call")
call_prima2 = Black_Scholes(S=S, K=call_K2, T=T, r=r, sigma=sigma, option_type="call")

# Prima Neta
prima_neta_crb = call_prima1 - (call_ratio * call_prima2)

# Payoff
payoff_crb = -np.maximum(prices - call_K1, 0) + call_ratio * np.maximum(prices - call_K2, 0) + prima_neta_crb

# Put Ratio Backspread (Ratio 1:2): Vender Put (K1) + Comprar 2 Puts (K2) con K1 > K2 -> Débito/Crédito

# Definir Strikes
put_K1 = 105 # Venta del Put
put_K2 = 95 # Compra del Put
put_ratio = 2 # Ratio 1:2

# Cálculo de las Primas
put_prima1 = Black_Scholes(S=S, K=put_K1, T=T, r=r, sigma=sigma, option_type="put")
put_prima2 = Black_Scholes(S=S, K=put_K2, T=T, r=r, sigma=sigma, option_type="put")

# Prima Neta
prima_neta_prb = put_prima1 - (put_ratio * put_prima2)

# Payoff
payoff_prb = -np.maximum(put_K1 - prices, 0) + put_ratio * np.maximum(put_K2 - prices, 0) + prima_neta_prb

# Visualizar Estrategias
plt.figure(figsize=(22, 7), dpi=300)

# Call Ratio Backspread
plt.subplot(1, 2, 1)
plt.plot(prices, payoff_crb, "b-", lw=3, label="Payoff Total")
# Líneas de Referencia
plt.axhline(y=0, color="black", linestyle="--")
plt.axvline(x=S, color="black", linestyle="--", label=f"Precio actual ({S})")
plt.axvline(x=call_K1, color="red", linestyle="--", label=f"Strike Call Vendido ({call_K1})")
plt.axvline(x=call_K2, color="blue", linestyle="--", label=f"Strikes Calls Comprados ({call_K2})")
# Rellenar áreas de B/P
plt.fill_between(x=prices, y1=payoff_crb, y2=0, where=(payoff_crb >= 0), color="green", alpha=0.2)
plt.fill_between(x=prices, y1=payoff_crb, y2=0, where=(payoff_crb < 0), color="red", alpha=0.2)
# Agregar anotaciones (Máxima Pérdida)
max_perdida = abs(min(payoff_crb))
plt.annotate(text=f"Máxima Pérdida: -${max_perdida:.2f}", xy=(call_K2+1, -max_perdida), xytext=(call_K2 + 10, -max_perdida),
             arrowprops=dict(arrowstyle="->"), fontsize=12, fontstyle="oblique")
# Punto de Equilibrio
plt.axvline(x=call_K2 + max_perdida, linestyle="--", label=f"Punto de Equilibrio ({call_K2 + max_perdida:.2f})")
# Añadir Etiquetas
plt.title(f"Call Ratio Backspread 1:{call_ratio}\nVender 1 Call @ {call_K1}, Comprar {call_ratio} Calls @ {call_K2}")
plt.xlabel("Precio del Activo Subyacente")
plt.ylabel("Ganancia/Pérdida")
plt.legend()
plt.grid()

# Put Ratio Backspread
plt.subplot(1, 2, 2)
plt.plot(prices, payoff_prb, "r-", lw=3, label="Payoff Total")
# Líneas de Referencia
plt.axhline(y=0, color="black", linestyle="--")
plt.axvline(x=S, color="black", linestyle="--", label=f"Precio actual ({S})")
plt.axvline(x=put_K1, color="red", linestyle="--", label=f"Strike Put Vendido ({put_K1})")
plt.axvline(x=put_K2, color="blue", linestyle="--", label=f"Strikes Puts Comprados ({put_K2})")
# Rellenar áreas de B/P
plt.fill_between(x=prices, y1=payoff_prb, y2=0, where=(payoff_prb >= 0), color="green", alpha=0.2)
plt.fill_between(x=prices, y1=payoff_prb, y2=0, where=(payoff_prb < 0), color="red", alpha=0.2)
# Agregar anotaciones (Máxima Pérdida)
max_perdida = abs(min(payoff_prb))
plt.annotate(text=f"Máxima Pérdida: -${max_perdida:.2f}", xy=(put_K2-1, -max_perdida), xytext=(put_K2 -30, -max_perdida),
             arrowprops=dict(arrowstyle="->"), fontsize=12, fontstyle="oblique")
# Punto de Equilibrio
plt.axvline(x=put_K2 - max_perdida, linestyle="--", label=f"Punto de Equilibrio ({put_K2 - max_perdida:.2f})")
# Añadir Etiquetas
plt.title(f"Put Ratio Backspread 1:{put_ratio}\nVender 1 Put @ {put_K1}, Comprar {put_ratio} Puts @ {put_K2}")
plt.xlabel("Precio del Activo Subyacente")
plt.ylabel("Ganancia/Pérdida")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

# Recordatorio:
    
# Tabla Descriptiva
tabla_ratio_backspread = pd.DataFrame({
    
    "Estrategia": ["Call Ratio Backspread", "Put Ratio Backspread"],
    "Dirección Esperada": ["Fuertemente Alcista", "Fuertemente Bajista"],
    "Tipo": ["Débito o Crédito", "Débito o Crédito"],
    "Máx Ganancia": ["Ilimitada (si sube mucho)", "Ilimitada (si baja mucho)"],
    "Máx Pérdida": ["Limitada"] * 2,
    "Posiciones": [
        
        "Vender 1 Call ITM o ATM (K1) + Comprar 2 Calls OTM (K2) | K1 < K2",
        "Vender 1 Put ITM o ATM (K1) + Comprar 2 Puts OTM (K2) | K1 > K2"
        
        ],
    "Puntos de Equilibrio": [
        
        "K2 + pérdida máxima",
        "K2 - pérdida máxima"
        
        ]
    
    })

print(tabla_ratio_backspread)
