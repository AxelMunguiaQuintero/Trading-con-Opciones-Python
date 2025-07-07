# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Introducción Teórica: ¿Qué es Vega?
print("""
Vega mide la sensibilidad del precio de una opción respecto a cambios en la volatilidad del activo subyacente.

Es decir, responde a la pregunta: ¿Cuánto podría variar el valor de la opción si la volatilidad cambia un 1%?

Conceptualmente:
    - Vega > 0 tanto para Calls como para Puts.
    - Cuanto mayor sea Vega, más expuesta está la opción a la volatilidad.
    - Las Opciones ATM tienen la mayor vega.
    - Vega es más alta cuando falta mucho tiempo para el vencimiento.

Vega también nos dice cuánto vale la incertidumbre. Si el mercado se vuelve más volatil, las primas suben.      
""")

# Función para calcular Vega
def calcular_vega(S, K, T, r, sigma):
    
    """
    Calcula Vega de una opción europea (Call o Put).
    Devuelve la sensibilidad del precio ante un cambio del 1% en la volatilidad.
    """
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    
    return vega / 100 # Vega por cambio del 1% en sigma

# Ejemplo Práctico
S = 100
K = 100
T = 0.5
r = 0.05
sigma = 0.30
# Calcular Vega
vega = calcular_vega(S, K, T, r, sigma)
print(f"Valor de Vega: {vega:.6f}")

# Visualización de Vega en Función del Precio del Subyacente
def graficar_vega(S_min=50, S_max=150, K=100, T=0.5, r=0.05, sigma=0.20):
    
    """
    Grafica la Vega de una opción respecto al precio del subyacente.
    """
    
    # Definir rango de precios y calcular vega
    precios = np.linspace(S_min, S_max, 300)
    vegas = [calcular_vega(S, K, T, r, sigma) for S in precios]
    # Plot
    plt.figure(figsize=(22, 6), dpi=300)
    plt.plot(precios, vegas, label=f"Vega (T={int(T * 365)} días)", color="purple")
    plt.axvline(K, linestyle="--", color="gray", label="Precio Strike")
    plt.title("Vega vs Precio del Subyacente")
    plt.xlabel("Precio del Activo Subyacente")
    plt.ylabel("Vega (Cambio por 1% en Volatilidad)")
    plt.grid()
    plt.legend()
    plt.show()
    
# Graficar Comportamiento de Vega
graficar_vega()

# Comparación de Vega con diferentes tiempos a vencimiento
def graficar_vega_multiples_vencimientos(K=100, sigma=0.25, r=0.01):
    
    """
    Compara Vega para distintos vencimientos.
    """

    # Definir rangos de los precios
    precios = np.linspace(60, 140, 300)
    vencimientos_dias = [15, 60, 180]
    colores = ["blue", "green", "red"]
    # Crear Plot
    plt.figure(figsize=(22, 6), dpi=300)
    # Iterar en Vencimientos
    for i, T_dias in enumerate(vencimientos_dias):
        T = T_dias / 365
        vegas = [calcular_vega(S, K, T, r, sigma) for S in precios]
        plt.plot(precios, vegas, label=f"{T_dias} días", color=colores[i])
    # Agregar etiquetas al plot
    plt.axvline(K, label="Strike", color="gray", linestyle="--")
    plt.title("Vega en Función del Precio - Diferentes Vencimientos")
    plt.xlabel("Precio del Subyacente")
    plt.ylabel("Vega")
    plt.legend()
    plt.grid()
    plt.show()
    
# Ejecutar Plot
graficar_vega_multiples_vencimientos()

# Evolución de Vega con el Tiempo
def graficar_vega_vs_tiempo():
    
    """
    Muestra cómo evoluciona Vega con el paso del tiempo.
    """

    # Definir parámetros
    S = 100
    K = 100
    r = 0.01
    sigma = 0.25
    T_list = np.linspace(start=0.01, stop=1.0, num=365)
    # Calcular Vegas
    vegas = [calcular_vega(S, K, T, r, sigma) for T in T_list]
    # Plot
    plt.figure(figsize=(22, 6), dpi=300)
    T_list_dias = T_list * 365
    plt.plot(T_list_dias, vegas, color="darkorange")
    plt.title("Vega vs Tiempo a Vencimiento")
    plt.xlabel("Días al Vencimiento")
    plt.ylabel("Vega")
    plt.grid()
    plt.gca().invert_xaxis()
    plt.show()
    
# Visualizar Evolución de Vega
graficar_vega_vs_tiempo()

# Cómo cambia el precio de la opción con la volatilidad
def impacto_volatilidad_en_precios(S=100, K=100, T=0.5, r=0.01):
    
    """
    Simula cómo cambia el precio del Calls y Puts cuando la volatilidad cambia.
    """
    
    # Crear Rangos de Volatilidades
    volatilidades = np.linspace(start=0.05, stop=1, num=100) # De 5% a 100%
    precios_call = []
    precios_put = []
    # Iterar en los niveles de volatilidad
    for sigma in volatilidades:
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        precios_call.append(call)
        precios_put.append(put)
        
    # Crear Figura
    plt.figure(figsize=(24, 8), dpi=300)
    plt.plot(volatilidades * 100, precios_call, label="Precio Call", color="blue")
    plt.plot(volatilidades * 100, precios_put, label="Precio Put", color="orange")
    plt.title("Efecto de la Volatilidad en el Precio de Opciones")
    plt.xlabel("Volatilidad")
    plt.ylabel("Precio de la Opción")
    plt.grid()
    plt.legend()
    plt.show()

# Visualizar Precio de la Opción con distintos niveles de Volatilidad
impacto_volatilidad_en_precios()

# Recordatorio:
#   - A mayor volatilidad esperada, mayor será el valor de la opción (mayor prima).
#   - Las Opciones ATM y con mayor tiempo a vencimiento tienen más vega.
#   - Vega es esencial en estrategias de volatilidad: straddle, strangle, calendar spreads, etc.
#   - Los compradores de Opciones se benefician de aumentos de volatilidad (Vega Positiva).
#   - Los vendedores están expuestos negativamente si la volatilidad sube inesperadamente.
