# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Parámetros del subyacente
S0 = 100
r = 0.05
sigma = 0.25
T = 0.5

# Simular Rango de Precios al Vencimiento
precios = np.linspace(start=50, stop=150, num=500)

# Definición de cada posición
spreads = {
    
    # Estrategia: (strike inferior, strike superior, tipo de opción a utilizar, posición 1, posición 2)
    "Bull Call Spread": (90, 110, "call", "long", "short"),  # Comprar Call K1 = 90, Vender Call K2 = 110 - Débito
    "Bear Call Spread": (90, 110, "call", "short", "long"),  # Vender Call K1 = 90, Comprar Call K2 = 110 - Crédito
    "Bull Put Spread": (90, 110, "put", "long", "short"),  # Comprar Put K1 = 90, Vender Put K2 = 110 - Crédito
    "Bear Put Spread": (90, 110, "put", "short", "long"),  # Vender Put K1 = 90, Comprar Put K2 = 110 - Débito
    
    } # K1 = 90, K2 = 110 Para todos los casos

# Modelo de BSM
def Black_Scholes_Merton(S, K, T, r, sigma, q=0, tipo="call"):
    
    """
    Calcula el precio de una opción europea usando el Modelo de BSM
    """
    
    # Calcular
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # Validar Tipo de Opción
    if tipo == "call":
        precio = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        precio = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        
    return precio

# Calcular primas de cada spread
primas = {}
for nombre, (K1, K2, tipo, posicion1, posicion2) in spreads.items():
    prima1 = Black_Scholes_Merton(S=S0, K=K1, T=T, r=r, sigma=sigma, q=0, tipo=tipo)
    prima2 = Black_Scholes_Merton(S=S0, K=K2, T=T, r=r, sigma=sigma, q=0, tipo=tipo)
    primas[nombre] = (prima1, prima2)
    
# Colores para cada estrategia
colores = {
    
    "Bull Call Spread": "#1f77b4", # Azul
    "Bear Call Spread": "#ff7f0e", # Naranja
    "Bull Put Spread": "#2ca02c",  # Verde
    "Bear Put Spread": "#d62728"   # Rojo
    
    }

# Crear Subplots
fig, axs = plt.subplots(2, 2, figsize=(22, 10), dpi=300)
fig.suptitle("Payoff de Vertical Spreads al Vencimiento", fontsize=20, fontweight="bold", color="#333333")
fig.patch.set_facecolor("#f9f9f9")

# Iterar para cada estrategia y graficar en su subplot correspondiente
for ax, (nombre, (K1, K2, tipo, posicion1, posicion2)) in zip(axs.flatten(), spreads.items()):
    
    # Calcular Payoff de cada opción
    if tipo == "call":
        payoff1 = np.maximum(precios - K1, 0)
        payoff2 = np.maximum(precios - K2, 0)
    else: 
        payoff1 = np.maximum(K1 - precios, 0)
        payoff2 = np.maximum(K2 - precios, 0)
        
    # Obtener primas correspondientes
    prima1, prima2 = primas[nombre]

    # Revisar posición 1
    if posicion1 == "long":
        valor1 = payoff1 - prima1
    else:
        valor1 = -payoff1 + prima1
            
    # Revisar posición 2
    if posicion2 == "long":
        valor2 = payoff2 - prima2
    else:
        valor2 = -payoff2 + prima2
        
    # Payoff Total
    payoff_total = valor1 + valor2
    
    # Máxima ganancia y pérdida
    max_gain = np.max(payoff_total)
    max_loss = np.min(payoff_total)
        
    # Graficar Diagramas de Pago para Cada Estrategia
    color = colores[nombre]
    ax.plot(precios, payoff_total, label=nombre, color=color, lw=3.5, alpha=0.85)
    # Agregar líneas informativas
    ax.axvline(x=K1, color=color, ls="--", lw=2, alpha=0.7, label=f"Strike 1: {K1}")
    ax.axvline(x=K2, color=color, ls="--", lw=2, alpha=0.7, label=f"Strike 2: {K2}")
    ax.axvline(x=S0, color="black", lw=2.5, ls="-.", label="Precio Subyacente")
    ax.axhline(y=0, color="gray", lw=1.2, ls="--", alpha=0.8)
    # Rellenar áreas de beneficio/pérdida
    ax.fill_between(x=precios, y1=payoff_total, y2=0, where=(payoff_total>=0), color=color, alpha=0.25, label="Ganancia")
    ax.fill_between(x=precios, y1=payoff_total, y2=0, where=(payoff_total<0), color="gray", alpha=0.15, label="Pérdida")
    # Mejorar la estética del gráfico
    ax.set_title(f"{nombre} - Payoff al Vencimiento", fontsize=16, fontweight="bold", color=color)
    ax.set_xlabel("Precio Subyacente", fontsize=13)
    ax.set_ylabel("Ganancia / Pérdida ($)", fontsize=13)
    ax.grid(True, linestyle="--", alpha=0.4)
    # Establecer límites en el eje y
    margen = max(abs(payoff_total)) * 1.2
    ax.set_ylim(-margen, margen)
    ax.legend(fontsize=11, loc="upper left" if "Bull" in nombre else "upper right")
    
    # Anotar máximos
    valor_x1 = precios[-1] - 30 if "Bull" in nombre else precios[0] + 5
    valor_x2 = precios[0] + 3 if "Bull" in nombre else precios[-1] - 30
    ax.text(x=valor_x1, y=max_gain * 0.75, s=f"Máx. Ganancia: ${max_gain:.2f}", fontsize=12, color="darkgreen", weight="bold",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", boxstyle="round,pad=0.3"))
    ax.text(x=valor_x2, y=max_loss * 0.90, s=f"Pérdida Max: ${max_loss:.2f}", fontsize=12, color="darkred", weight="bold",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", boxstyle="round,pad=0.3"))
    
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Recordatorio:
    
# Tabla Comparativa de Estrategias
tabla = pd.DataFrame({
    
    "Estrategia": ["Bull Call Spread", "Bear Call Spread", "Bull Put Spread", "Bear Put Spread"],
    "Dirección Esperada": ["Alcista", "Bajista", "Alcista", "Bajista"],
    "Tipo": ["Débito", "Crédito", "Crédito", "Débito"],
    "Máx. Ganancia": ["Limitada"] * 4,
    "Máx. Pérdida": ["Limitada"] * 4,
    "Posiciones": [
        
        "Comprar Call (K1), Vender Call (K2)", # K1 < K2
        "Vender Call (K1), Comprar Call (K2)", # K1 < K2
        "Comprar Put (K1), Vender Put (K2)",   # K1 < K2
        "Vender Put (K1), Comprar Put (K2)"    # K1 < K2
        
        ],
    "Punto de Equilibrio": [
        
        "K1 + Débito Neto",
        "K1 + Crédito Neto",
        "K2 - Crédito Neto",
        "K2 - Débito Neto"
        
        ]
    
    })

print(tabla)
