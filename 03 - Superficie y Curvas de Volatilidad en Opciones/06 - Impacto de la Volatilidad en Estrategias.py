# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Definir función de BSM
def Black_Scholes_Merton(S, K, T, r, sigma, q, tipo = "call"):
    
    """
    Calcula la prima de una opción europea usando el modelo de Black-Scholes-Merton.
    """
    
    # Calcular d1 y d2
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # Calcular Prima
    prima = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2) if tipo == "call" else \
        K * np.exp(-r*T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        
    return prima

# Parámetros Iniciales
S_0 = 4
K = 4
sigma = 0.30
r = 0.05
T_total = 30 / 365

# Encontrar Precio para un Put en Condicionales Normales
prima = Black_Scholes_Merton(S=S_0, K=K, T=T_total, r=r, sigma=sigma, q=0, tipo="put")
prima = round(prima, 4)
print(f"El precio justo para una posición Long Put sería de ${prima} dólares")

# Volver a calcular la prima en condiciones anormales (2 días después)
sigma_nueva = 9.0 # Volatilidad I. del 900%
S_nuevo = 8 # Nuevo Valor del Activo (La empres hizo pública una noticia favorable para ellos)
T_nuevo = (30 - 2) / 365
prima_nueva = Black_Scholes_Merton(S=S_nuevo, K=K, T=T_nuevo, r=r, sigma=sigma_nueva, q=0, tipo="put")
prima_nueva = round(prima_nueva, 4)
print(f"El nuevo precio justo para una posición Long Put sería de ${prima_nueva} dólares")

# Calcular Ganancia
ganancia_neta = prima_nueva - prima
ganancia_porcentaje = (ganancia_neta / prima) * 100
print(f"Ganancia Total en Porcentaje = {ganancia_porcentaje:,.4f}%")

# Rango de Volatilidades
volatilidades_futuras = np.linspace(start=0.30, stop=9.0, num=200)
# Calcular la utilidad para cada simulación
ganancias = []
for sigma_futuro in volatilidades_futuras:
    prima_futura = Black_Scholes_Merton(S=S_nuevo, K=K, T=T_nuevo, r=r, sigma=sigma_futuro, q=0, tipo="put")
    # Calcular Ganancia o Pérdida en Porcentaje con respecto a la prima
    ganancia_pct = ((prima_futura - prima) / prima) * 100
    ganancias.append(ganancia_pct)
    
# Convertir a array las volatilidades
volatilidades_futuras = np.array(volatilidades_futuras)
ganancias = np.array(ganancias)

# Gráfico
plt.figure(figsize=(22, 7), dpi=300)

# Curva de Ganancia
plt.plot(volatilidades_futuras * 100, ganancias, color="black", lw=2, label="Ganancia/Pérdida (%)")
plt.fill_between(x=volatilidades_futuras*100, y1=ganancias, y2=0, where=(ganancias>=0), color="lightgreen", alpha=0.4)
plt.fill_between(x=volatilidades_futuras*100, y1=ganancias, y2=0, where=(ganancias<0), color="salmon", alpha=0.4)

# Línea vertical en la volatilidad inicial
plt.axvline(sigma * 100, color="navy", linestyle="--", label=f"Volatilidad Inicial: {sigma*100:.0f}%")
plt.axhline(0, color="gray", linestyle="--", lw=1)

plt.title("Ganancia/Pérdida de una Opción Put vs Volatilidad Implícita", fontsize=16)
plt.xlabel("Volatilidad Implícita (%)", fontsize=14)
plt.ylabel("Ganancia o Pérdida (%)", fontsize=14)
plt.grid(linestyle="--", alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()

# Recordatorio:
#   - La Volatilidad Implícita puede aumentar significativamente el valor de una opción, incluso si está fuera del dinero,
#     debido a la expectativa de movimientos bruscos en el precio del activo.
