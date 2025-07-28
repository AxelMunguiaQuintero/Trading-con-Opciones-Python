# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Parámetros de las estrategias
S = 100
r = 0.05
sigma = 0.25
T = 0.5

# Definición de Strikes para Iron Condor (4 Strikes)
K1, K2, K3, K4 = 80, 90, 110, 120
#   - Inverse Iron Condor: Vender Put OTM (K1) + Comprar Put OTM (K2) + Comprar Call OTM (K3) + Vender Call OTM (K4)
#     con K1 < K2 < K3 < K4 -> Se paga un débito
#   - Iron Condor: Comprar Put OTM (K1) + Vender Put OTM (K2) + Vender Call OTM (K3) + Comprar Call OTM (K4)
#     con K1 < K2 < K3 < K4 -> Se recibe un crédito

# Definición de Strikes para Iron Butterfly (3 Strikes)
K1_b, K2_b, K3_b = 90, 100, 110
#   - Inverse Iron Butterfly: Vender Put OTM (K1) + Comprar Put ATM (K2) + Comprar Call ATM (K2) + Vender Call OTM (K3)
#     con K1 < K2 < K3 -> Se paga un débito
#   - Iron Butterfly: Comprar Put OTM (K1) + Vender Put ATM (K2) + Vender Call ATM (K2) + Comprar Call OTM (K3)
#     con K1 < K2 < K3 -> Se recibe un crédito

# Calcular Primas de Forma Teórica
def Black_Scholes(S, K, T, r, sigma, tipo="call"):
    
    """
    Calcula el precio justo de una opción.
    """
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if tipo == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
# Primas para Iron Condor e Inverse Iron Condor
put_k1 = Black_Scholes(S=S, K=K1, T=T, r=r, sigma=sigma, tipo="put")
put_k2 = Black_Scholes(S=S, K=K2, T=T, r=r, sigma=sigma, tipo="put")
call_k3 = Black_Scholes(S=S, K=K3, T=T, r=r, sigma=sigma, tipo="call")
call_k4 = Black_Scholes(S=S, K=K4, T=T, r=r, sigma=sigma, tipo="call")

# Primas para Iron Butterfly e Inverse Iron Butterfly
put_k1_b = Black_Scholes(S=S, K=K1_b, T=T, r=r, sigma=sigma, tipo="put")
put_k2_b = Black_Scholes(S=S, K=K2_b, T=T, r=r, sigma=sigma, tipo="put")
call_k2_b = Black_Scholes(S=S, K=K2_b, T=T, r=r, sigma=sigma, tipo="call")
call_k3_b = Black_Scholes(S=S, K=K3_b, T=T, r=r, sigma=sigma, tipo="call")

# Rango de Precios al Vencimiento
precios = np.linspace(60, 140, 1000)

# Función payoff de la estrategia Iron Condor (al vencimiento)
payoff_ic = (
    
    np.maximum(K1 - precios, 0) - put_k1 +   # Comprar Put OTM K1 (Long Put)
    -np.maximum(K2 - precios, 0) + put_k2 +  # Vender Put OTM K2 (Short Put)
    -np.maximum(precios - K3, 0) + call_k3 + # Vender Call OTM K3 (Short Call)
    np.maximum(precios - K4, 0) - call_k4    # Comprar Call OTM K4 (Long Call)
    
    )

# Inverse Iron Condor
payoff_inverse_ic = -payoff_ic

# Función payoff de la estrategia Iron Butterfly
payoff_ib = (
    
    np.maximum(K1_b - precios, 0) - put_k1_b +       # Comprar Put OTM K1 (Long Put)
    -np.maximum(K2_b - precios, 0) + put_k2_b +      # Vender Put ATM K2 (Short Put)
    -np.maximum(precios - K2_b, 0) + call_k2_b +     # Vender Call ATM K2 (Short Call)
    np.maximum(precios - K3_b, 0) - call_k3_b        # Comprar Call OTM K3 (Long Call)
    
    )

# Inverse Iron Butterfly
payoff_inverse_ib = -payoff_ib

# Definir Función para graficar los Diagramas de Pago
def plot_payoff(ax, precios_rango, payoff, title, color_line, color_fill_positivo, color_fill_negativo, strikes):
    
    """
    Función para graficar el payoff de una estrategia en un eje dado.
    """
    
    # Línea del perfil de ganancias al vencimiento
    ax.plot(precios_rango, payoff, color=color_line, lw=2, label="Payoff al vencimiento")
    
    # Áreas de Ganancia y Pérdida al vencimiento
    ax.fill_between(x=precios_rango, y1=payoff, y2=0, where=(payoff >= 0), alpha=0.2, color=color_fill_positivo)
    ax.fill_between(x=precios_rango, y1=payoff, y2=0, where=(payoff < 0), alpha=0.2, color=color_fill_negativo)    
    
    ax.axhline(0, color="black", linestyle="--")
    
    # Anotaciones de Strikes con Flechas
    for strike in strikes:
        ax.annotate(f"Strike\n{strike}", xy=(strike, 0), xytext=(strike, -1.5), ha="center", 
                    arrowprops=dict(arrowstyle="->"))
    
    # Configuración de título y etiquetas
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Precio del Subyacente", fontsize=11)
    ax.grid()
    ax.legend(fontsize=10, loc="center right")
    if ax in [axs[0,0], axs[1, 0]]:
        ax.set_ylabel("Ganancia/Pérdida", fontsize=11)
        
    # Anotaciones de máximo beneficio y pérdida
    max_profit = max(payoff)
    max_loss = min(payoff)
    ax.text(95, max_profit * 0.80, f"Máx Beneficio: {max_profit:.1f}", bbox=dict(facecolor="lightgreen", alpha=0.7))
    ax.text(95, max_loss * 0.9, f"Máx Pérdida: {abs(max_loss):.1f}", bbox=dict(facecolor="lightcoral", alpha=0.7))  

# Crear figura con 2 filas y 2 columnas de subplots
fig, axs = plt.subplots(2, 2, figsize=(24, 10), dpi=300)
fig.suptitle("Estrategias de Opciones: Iron Condor y Iron Butterfly", fontsize=18)

# Inverse Iron Condor: Estrategia de Débito
plot_payoff(ax=axs[0, 0], precios_rango=precios, payoff=payoff_inverse_ic, title="Inverse Iron Condor", 
            color_line="green", color_fill_positivo="lightgreen", color_fill_negativo="lightcoral", strikes=[K1, K2, K3, K4])

# Iron Condor: Estrategia de Crédito
plot_payoff(ax=axs[0, 1], precios_rango=precios, payoff=payoff_ic, title="Iron Condor", 
            color_line="red", color_fill_positivo="lightgreen", color_fill_negativo="lightcoral", strikes=[K1, K2, K3, K4])

# Inverse Iron Butterfly: Estrategia de Débito
plot_payoff(ax=axs[1, 0], precios_rango=precios, payoff=payoff_inverse_ib, title="Inverse Iron Butterfly", 
            color_line="blue", color_fill_positivo="lightgreen", color_fill_negativo="lightcoral", strikes=[K1_b, K2_b, K3_b])

# Iron Butterfly: Estrategia de Crédito
plot_payoff(ax=axs[1, 1], precios_rango=precios, payoff=payoff_ib, title="Iron Butterfly", 
            color_line="purple", color_fill_positivo="lightgreen", color_fill_negativo="lightcoral", strikes=[K1_b, K2_b, K3_b])

plt.tight_layout()
plt.show()

# Recordatorio:
    
# Tabla Descriptiva para Iron Condor
tabla_iron_condor = pd.DataFrame({
    
    "Estrategia": ["Inverse Iron Condor", "Iron Condor"],
    "Dirección Esperada": ["Movimiento Fuerte (alta volatilidad)", "Neutral (Baja Volatilidad)"],
    "Tipo": ["Débito", "Crédito"],
    "Máx Ganancia": ["Limitada", "Limitada"],
    "Máx Pérdida": ["Limitada", "Limitada"],
    "Posiciones": [
        
        "Vender Put OTM (K1) + Comprar Put OTM (K2) + Comprar Call OTM (K3) + Vender Call OTM (K4) | K1<K2<K3<K4",
        "Comprar Put OTM (K1) + Vender Put OTM (K2) + Vender Call OTM (K3) + Comprar Call OTM (K4) | K1<K2<K3<K4"
        
        ],
    "Puntos de Equilibrio": [
        
        "K2 - prima neta | K3 + prima neta",
        "K2 - prima neta | K3 + prima neta"
        
        ]
    
    })

print("Iron Condor")
print("-----------")
print(tabla_iron_condor)

# Tabla Descriptiva para Iron Butterfly
tabla_iron_butterfly = pd.DataFrame({
    
    "Estrategia": ["Inverse Iron Butterfly", "Iron Butterfly"],
    "Dirección Esperada": ["Movimiento Fuerte (alta volatilidad)", "Neutral (Baja Volatilidad)"],
    "Tipo": ["Débito", "Crédito"],
    "Máx Ganancia": ["Limitada", "Limitada"],
    "Máx Pérdida": ["Limitada", "Limitada"],
    "Posiciones": [
        
        "Vender Put OTM (K1) + Comprar Put ATM (K2) + Comprar Call ATM (K2) + Vender Call OTM (K3) | K1<K2<K3",
        "Comprar Put OTM (K1) + Vender Put ATM (K2) + Vender Call ATM (K2) + Comprar Call OTM (K3) | K1<K2<K3"
        
        ],
    "Puntos de Equilibrio": [
        
        "K1 + prima neta | K3 - prima neta",
        "K2 - prima neta | K2 + prima neta"
        
        ]
    
    })

print("Iron Butterfly")
print("-----------")
print(tabla_iron_butterfly)
