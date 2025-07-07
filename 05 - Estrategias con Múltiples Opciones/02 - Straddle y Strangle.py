# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Definir parámetros
S0 = 100
T = 30 / 365
r = 0.05
sigma = 0.25
# Rango de Precios
precio_activo = np.linspace(80, 120, 500)

# Definir fórmula
def Black_Scholes(S, K, T, r, sigma, tipo="call"):
    
    """
    Función que calcula el precio justo de una prima
    """
    
    # Calcular
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if tipo == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
# Strikes para Straddle
K_straddle = 100 
# Strikes para Strangle
K_put_strangle, K_call_strangle = 95, 105

# Obtener Primas para Estrategia de Straddle:
#   - Long Straddle: Comprar Call ATM + Comprar Put ATM -> Pagas un débito por esta posición
#   - Short Straddle: Vender Call ATM + Vender Put ATM -> Recibes un crédito por esta posición
prima_call_straddle = Black_Scholes(S=S0, K=K_straddle, T=T, r=r, sigma=sigma, tipo="call")
prima_put_straddle = Black_Scholes(S=S0, K=K_straddle, T=T, r=r, sigma=sigma, tipo="put")

# Obtener Primas para Estrategia Strangle:
#   - Long Strangle: Comprar Call OTM (K2) + Comprar Put OTM (K1) con K1 < K2 -> Pagas un débito por esta posición
#   - Short Strangle: Vender Call OTM (K2) + Vender Put OTM (K1) con K1 < K2 -> Recibes un crédito por esta posición
prima_call_strangle = Black_Scholes(S=S0, K=K_call_strangle, T=T, r=r, sigma=sigma, tipo="call")
prima_put_strangle = Black_Scholes(S=S0, K=K_put_strangle, T=T, r=r, sigma=sigma, tipo="put")

# Realizar Plot
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(22, 10), dpi=300)
fig.suptitle("Estrategias de Opciones: Straddles y Strangles con Valor Actual y Payoff", fontsize=18, fontweight="bold")

# Definir función auxiliar
def plot_payoff_vs_valor(ax, precios, payoff, valor_actual, strikes, titulo, color):
    
    """
    Función que genera el diagrama de pago para cada Estrategia
    """

    # Plot
    ax.plot(precios, payoff, color="black", label="Payoff al Vencimiento", lw=2)
    ax.plot(precios, valor_actual, "b--", lw=2, label="Valor Actual (Market-to-Market)")
    ax.axhline(y=0, color="black", lw=0.8)
    # Crear líneas en los strikes
    for n, s in enumerate(strikes):
        ax.axvline(x=s, color="gray", linestyle="--", label=f"Strike {n + 1}: {s}")
    # Rellenar áreas de beneficio y pérdida
    ax.fill_between(x=precios, y1=0, y2=payoff, where=(payoff >= 0), color="green", alpha=0.3)
    ax.fill_between(x=precios, y1=0, y2=payoff, where=(payoff < 0), color="red", alpha=0.3)
    # Agregar estética
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xlabel("Precio del Activo al Vencimiento")
    ax.set_ylabel("Ganancia / Pérdida")
    ax.legend()
    
# Long Straddle (Comprar Call y Put ATM)
payoff_ls = np.maximum(precio_activo - K_straddle, 0) + np.maximum(K_straddle - precio_activo, 0) \
    - (prima_call_straddle + prima_put_straddle)
valor_ls = Black_Scholes(S=precio_activo, K=K_straddle, T=T, r=r, sigma=sigma, tipo="call") + \
    Black_Scholes(S=precio_activo, K=K_straddle, T=T, r=r, sigma=sigma, tipo="put")
plot_payoff_vs_valor(ax=axs[0, 0], precios=precio_activo, payoff=payoff_ls, valor_actual=valor_ls, strikes=[K_straddle], 
                     titulo=f"Long Straddle\nPrima Call={prima_call_straddle:.2f}, Put={prima_put_straddle:.2f}\n" + \
                         f"Total Pagado (Débito) = {prima_call_straddle + prima_put_straddle:.3f}", color="green")
    
# Short Straddle (Vender Call y Put ATM)
payoff_ss = -np.maximum(precio_activo - K_straddle, 0) - np.maximum(K_straddle - precio_activo, 0) \
    + (prima_call_straddle + prima_put_straddle)
valor_ss = -(Black_Scholes(S=precio_activo, K=K_straddle, T=T, r=r, sigma=sigma, tipo="call") + \
    Black_Scholes(S=precio_activo, K=K_straddle, T=T, r=r, sigma=sigma, tipo="put"))
plot_payoff_vs_valor(ax=axs[0, 1], precios=precio_activo, payoff=payoff_ss, valor_actual=valor_ss, strikes=[K_straddle], 
                     titulo=f"Short Straddle\nPrima Call={prima_call_straddle:.2f}, Put={prima_put_straddle:.2f}\n" + \
                         f"Total Recibido (Crédito) = {prima_call_straddle + prima_put_straddle:.3f}", color="red")
    
# Long Strangle
payoff_lsg = np.maximum(precio_activo - K_call_strangle, 0) + np.maximum(K_put_strangle - precio_activo, 0) \
    - (prima_call_strangle + prima_put_strangle)
valor_lsg = Black_Scholes(S=precio_activo, K=K_call_strangle, T=T, r=r, sigma=sigma, tipo="call") + \
    Black_Scholes(S=precio_activo, K=K_put_strangle, T=T, r=r, sigma=sigma, tipo="put")
plot_payoff_vs_valor(ax=axs[1, 0], precios=precio_activo, payoff=payoff_lsg, valor_actual=valor_lsg, 
                     strikes=[K_put_strangle, K_call_strangle], 
                     titulo=f"Long Strangle\nPrima Call={prima_call_strangle:.2f}, Put={prima_put_strangle:.2f}", color="green")

# Short Strangle
payoff_ssg = -np.maximum(precio_activo - K_call_strangle, 0) - np.maximum(K_put_strangle - precio_activo, 0) \
    + (prima_call_strangle + prima_put_strangle)
valor_ssg = -(Black_Scholes(S=precio_activo, K=K_call_strangle, T=T, r=r, sigma=sigma, tipo="call") + \
    Black_Scholes(S=precio_activo, K=K_put_strangle, T=T, r=r, sigma=sigma, tipo="put"))
plot_payoff_vs_valor(ax=axs[1, 1], precios=precio_activo, payoff=payoff_ssg, valor_actual=valor_ssg, 
                     strikes=[K_put_strangle, K_call_strangle], 
                     titulo=f"Short Strangle\nPrima Call={prima_call_strangle:.2f}, Put={prima_put_strangle:.2f}", color="red")

plt.tight_layout()
plt.show()

# Recordatorio:
    
# Tabla Descriptiva de Estrategias
tabla_estrategias = pd.DataFrame({
    
    "Estrategia": ["Long Straddle", "Short Straddle", "Long Strangle", "Short Strangle"],
    "Dirección Esperada": ["Neutral (Alta Volatilidad)", "Neutral (Baja Volatilidad)",
                           "Neutral (Alta Volatilidad)", "Neutral (Baja Volatilidad)"],
    "Tipo": ["Débito", "Crédito", "Débito", "Crédito"],
    "Máx. Ganancia": ["Ilimitada (Call + Put)", "Limitada (Primas Recibidas)", "Ilimitada (Call y Put)", "Limitada (Primas Recibidas)"],
    "Máx. Pérdida": ["Limitada (Primas Pagadas)", "Ilimitada", "Limitada (Primas Pagadas)", "Ilimitada"],
    "Posiciones": ["Comprar Call (K) + Comprar Put (K)", "Vender Call (K) + Vender Put (K)",
                   "Comprar Call (K2) + Comprar Put (K1) | K1 < K2",
                   "Vender Call (K2) + Vender Put (K1) | K1 < K2"],
    "Punto de Equilibrio": ["K +/- (Prima Call + Prima Put)", "K +/- (Prima Call + Prima Put)",
                            "K1 - Prima Neta (Put) | K2 + Prima Neta (Call)",
                            "K1 - Prima Neta (Put) | K2 + Prima Neta (Call)"]
    
    })
print(tabla_estrategias)
