# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Introducción Conceptual
print("""
Rho mide la sensibilidad del precio de una opción ante variaciones en la tasa de interés libre de riesgo.
En otras palabras, mide cuánto cambia el valor de una opción (no del activo subyacente) cuando la tasa de
interés libre de riesgo aumenta en 1% (o 0.01 en términos decimales), manteniendo todo lo demás constante.

- Cuando suben las tasas de interés, las opciones Call tienden a subir de valor.
- Los Put tienden a bajar su valor.

Un aumneto en las tasas reduce el valor presente del precio de ejercicio (strike), lo cual favorece a los 
Calls (que comprarían el activo en el futuro) y perjudica a los Puts (que venden el activo en el futuro).

Regla General:
    - Rho de un Call: Positivo
    - Rho de un Put: Negativo
""")

# Función para Calcular Rho
def calcular_rho(S, K, T, r, sigma, tipo_opcion):
    
    """
    Calcula Rho: Sensibilidad del precio de la opción ante cambios en la tasa de interés.
    """
    
    # d1 y d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if tipo_opcion == "call":
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    elif tipo_opcion == "put":
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    else:
        raise ValueError("El tipo de la opción debe ser 'call' o 'put'")
        
    return rho / 100 # Por cada 1% de cambio en tasa

# Ejemplo de Rho
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.30
# Calcular Rho
rho_call = calcular_rho(S, K, T, r, sigma, tipo_opcion="call")
rho_put = calcular_rho(S, K, T, r, sigma, tipo_opcion="put")

# Desplegar Valores
print("Rho para un call:", rho_call)
print("Rho para un Put:", rho_put)

# Visualización intuitiva: Cómo cambia el valor de la opción ante diferentes tasas
def graficar_rho_vs_Tasas(S=100, K=100, T=1, sigma=0.3):
    
    """
    Grafica cómo se comporta el valor de Rho frente a distintas tasas de interés.
    """

    # Calcular Primas de Opciones (Calls y Puts)
    tasas = np.linspace(0.001, 0.10, 200) # Tasas desde 0.1% hasta 10% Anual
    rhos_call = [calcular_rho(S, K, T, r, sigma, tipo_opcion="call") for r in tasas]
    rhos_put = [calcular_rho(S, K, T, r, sigma, tipo_opcion="put") for r in tasas]
    # Definir Plot
    plt.figure(figsize=(22, 6), dpi=300)
    plt.plot(tasas * 100, rhos_call, label="Rho Call", color="navy")
    plt.plot(tasas * 100, rhos_put, label="Rho Put", color="crimson")
    plt.axhline(0, color="gray", linestyle="--")
    plt.title("Rho vs Tasa de Interés")
    plt.xlabel("Tasa de Interés (%)")
    plt.ylabel("Rho (Cambio en precio de la opción)")
    plt.legend()
    plt.grid()
    plt.show()
    
# Visualizar Cambio
graficar_rho_vs_Tasas()

# Exploración Visual: Comparativa en diferentes Vencimientos
def graficar_rho_por_vencimiento(S=100, K=100, r=0.05, sigma=0.3):
    
    """
    Visualiza cómo evoluciona Rho según el tiempo a vencimiento.
    """
    
    # Calcular
    vencimientos = np.linspace(0.01, 2, 100)
    rho_call_vals = [calcular_rho(S, K, T, r, sigma, tipo_opcion="call") for T in vencimientos]
    rho_put_vals = [calcular_rho(S, K, T, r, sigma, tipo_opcion="put") for T in vencimientos]
    # Plot
    plt.figure(figsize=(22, 6), dpi=300)
    plt.plot(vencimientos * 365, rho_call_vals, label="Rho Call", color="navy")
    plt.plot(vencimientos * 365, rho_put_vals, label="Rho Put", color="crimson")
    plt.axhline(0, color="gray", linestyle="--")
    plt.title("Rho vs Tiempo a Vencimiento")
    plt.xlabel("Días hasta Vencimiento")
    plt.ylabel("Rho (Cambio en precio de la opción)")
    plt.legend()
    plt.grid()
    plt.show()
    
# Visualizar análisis
graficar_rho_por_vencimiento()

# Simulación económica realista: ¿Qué pasa si suben las tasas?
def simular_impacto_tasas_en_precios(S=100, K=100, T=1, sigma=0.25):
    
    """
    Simula el cambio en precios de Calls y Puts ante distintos niveles de tasa.
    """
    
    # Variar Tasas de Interés (0.1% a 10%)
    tasas = np.linspace(0.001, 0.10, 100)
    precios_call = []
    precios_put = []
    # Calcular
    for r in tasas:
        # Calcular Primas
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        precios_call.append(call)
        precios_put.append(put)
    # Plot
    plt.figure(figsize=(22, 6), dpi=300)
    plt.plot(tasas * 100, precios_call, label="Precio Call", color="blue")
    plt.plot(tasas * 100, precios_put, label="Precio Put", color="red")
    plt.title("Valor de la Opción vs Tasa de Interés")
    plt.xlabel("Tasa de Interés (%)")
    plt.ylabel("Valor de la Opción")
    plt.grid()
    plt.legend()
    plt.show()
    
# Visualizar cambio en el precio de la opción
simular_impacto_tasas_en_precios()

# Recordatorio:
#   - Comprador de Call: Se beneficia si las tasas suben -> Rho Positivo
#   - Comprador de Put: Se ve afectado negativamente si suben las tasas -> Rho Negativo
#   - Vendedor de Call: Pierde si suben las tasas
#   - Vendedor de Put: Se beneficia si suben las tasas
#   - Rho cobra importancia en opciones de largo plazo o en entornos de tasas cambiantes.
#   - En entornos de tasas cercanas a cero (como en 2020-2021), Rho era casi irrelevante.
#     Pero cuando las tasas suben, Rho puede ser una Griega decisiva (2023, 2024 y 2025).
