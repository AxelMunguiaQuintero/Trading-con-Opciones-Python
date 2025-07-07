# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as si

# Desplegar un breve resumen introductorio
print("""
En términos simples, Gamma nos dice **qué tan rápido cambia la Delta** cuando el precio del activo se mueve en
una unidad.

Interpretación:
    - Gamma mide la sensibilidad de Delta.
    - Si la Gamma es alta, significa que la Delta cambia rápidamente con movimientos pequeños en el precio del activo.

¿Para qué sirve?

Es especialmente importante cuando haces cobertura dinámica (delta hedging).
Una Gamma alta implica que tendrás que estar actualizando tu cobertura con mucha frecuencia, porque la Delta
ya no es constante: cambia con cada pequeño movimiento del mercado.      
""")

# Calcular Griega Gamma
def calcular_gamma(S, K, T, r, sigma): 
    
    """
    Calcula la Gamma de una opción europea usando el Modelo BS.
    """
    
    # Realizar cálculo
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    gamma = si.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    return gamma

# Realizar un ejemplo
S = 100
K = 100
T = 0.5
r = 0.05
sigma = 0.25
gamma = calcular_gamma(S, K, T, r, sigma)
print(f"Gamma: {gamma:.6f}")

# Análisis de Gamma con Diferentes Rangos de Precios
def graficar_gamma(S_min=50, S_max=150, K=100, T=0.5, r=0.05, sigma=0.25):
    
    """
    Grafica la Gamma de una opción respecto al precio del subyacente.
    """

    # Crear rango de precios y calcular gamma
    precios = np.linspace(S_min, S_max, 200)
    gammas = [calcular_gamma(S, K, T, r, sigma) for S in precios]
    # Generar Plot
    plt.figure(figsize=(22, 10), dpi=300)
    plt.plot(precios, gammas, label="Gamma", color="purple")
    plt.axvline(x=K, color="gray", linestyle="--", label="Precio Strike (K)")
    plt.title("Gamma vs Precio del Subyacente")
    plt.xlabel("Precio del Subyacente (S)")
    plt.ylabel("Gamma")
    plt.legend()
    plt.grid()
    plt.show()
    
# Ejecutar visualización
graficar_gamma()

# Análisis de Sensibilidad: Volatilidad y Tiempo
def analisis_sensibilidad_gamma():
    
    """
    Explora cómo cambia la Gamma con diferentes niveles de volatilidad y tiempo a vencimiento.
    
        - La Gamma es mayor cuando el subyacente está cerca del strike.
        - Gamma es simétrica en calls y puts europeas (ambas tienen mismo Gamma).
        - Cuando el tiempo a vencimiento es bajo y el subyacente es ≈ strike, la Gamma se vuelve muy alta.
    """
    
    # Definir parámetros
    r = 0.05
    K = 100
    volatilidades = [0.10, 0.30, 0.60]
    tiempos = [0.05, 0.5, 1.0]
    # Crear rangos de precios
    precios = np.linspace(50, 150, 200)
    
    # Generar gráfico
    plt.figure(figsize=(22, 10), dpi=300)
    # Iterar en Volatilidades y Tiempos
    for i, sigma in enumerate(volatilidades):
        # Generar Subplot
        plt.subplot(1, 3, i+1)
        for T in tiempos:
            # Calcular gammas con parámetros de la iteración
            gammas = [calcular_gamma(S, K, T, r, sigma) for S in precios]
            plt.plot(precios, gammas, label=f"T={T:.2f}")
        plt.axvline(K, color="gray", linestyle="--", label="Precio Strike (K)")
        plt.title(f"Gamma con Volatilidad = {sigma}")
        plt.xlabel("Precio del Subyacente")
        plt.ylabel("Gamma")
        plt.grid()
        plt.legend()
    
    plt.tight_layout()
    plt.show()

# Ejecutar análisis de sensibilidad
analisis_sensibilidad_gamma()

# Aplicación Práctica: Impacto en Delta Hedging considerando Gamma
def ejemplo_gamma_en_cobertura():
    
    """
    Este ejemplo muestra cómo varía la Delta y la Gamma de una opción dependiendo del tiempo
    hasta el vencimiento (T). Compararemos dos opciones (Calls europeas):
        
        - Una con vencimiento lejano (Gamma baja)
        - Otra con vencimiento cercano (Gamma alta)
        
    El objetivo es ilustrar por qué una opción con Gamma alta requiere ajustes más frecuentes en una
    estrategia de cobertura con Delta.
    """

    # Definir parámetros
    S_base = 100
    K = 100
    r = 0.05
    sigma = 0.30
    T_larga = 1 
    T_corta = 0.05 # 365 * .05 = 18.25 días
    
    # Simulamos un rango de precios del subyacente alrededor de S_base
    movimientos = np.linspace(-5, 5, 100)
    precios = S_base + movimientos
    
    # Listas para almacenar los resultados
    deltas_larga = []
    deltas_corta = []
    gammas_larga = []
    gammas_corta = []

    # Iterar en el movimiento de los precios
    for S in precios:
        # Calcular d1 para cada vencimiento
        d1_larga = (np.log(S / K)+(r + 0.5 * sigma ** 2) * T_larga) / (sigma * np.sqrt(T_larga))
        d1_corta = (np.log(S / K)+(r + 0.5 * sigma ** 2) * T_corta) / (sigma * np.sqrt(T_corta))
        
        # Calcular Delta
        delta_larga = si.norm.cdf(d1_larga)
        delta_corta = si.norm.cdf(d1_corta)
        
        # Calcular Gamma
        gamma_larga = si.norm.pdf(d1_larga) / (S * sigma * np.sqrt(T_larga))
        gamma_corta = si.norm.pdf(d1_corta) / (S * sigma * np.sqrt(T_corta))
        
        # Guardar Resultados
        deltas_larga.append(delta_larga)
        deltas_corta.append(delta_corta)
        gammas_larga.append(gamma_larga)
        gammas_corta.append(gamma_corta)

    # Gráficar Deltas
    plt.figure(figsize=(22, 6), dpi=300)
    plt.subplot(1, 2, 1)
    plt.plot(precios, deltas_larga, label="Delta (T largo)", color="green")
    plt.plot(precios, deltas_corta, label="Delta (T corto)", color="orange")
    plt.title("Comparación de Deltas")
    plt.xlabel("Precio del Subyacente")
    plt.ylabel("Delta")
    plt.axvline(100, linestyle="--", color="gray", alpha=0.7)
    plt.legend()
    plt.grid()

    # Gráficar Gammas
    plt.subplot(1, 2, 2)
    plt.plot(precios, gammas_larga, label="Gamma (T largo)", color="green", linestyle="--")
    plt.plot(precios, gammas_corta, label="Gamma (T corto)", color="orange", linestyle="--")
    plt.title("Comparación de Gamma")
    plt.xlabel("Precio del Subyacente")
    plt.ylabel("Gamma")
    plt.axvline(100, linestyle="--", color="gray", alpha=0.7)
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()
    
# Correr ejemplo de cobertura con delta y gamma
ejemplo_gamma_en_cobertura()

# Recordatorio:
#   - Una Gamma alta implica que la Delta cambiará rápidamente, haciendo que la cobertura con Delta requiera ajustes más 
#     frecuentes y precisos.
#   - Gamma es mayor en opciones cercanas al vencimiento y con baja volatilidad. Esto significa que el riesgo de cambios abruptos
#     en la Delta se concentra en estos casos, incrementando la complejidad y costo del manejo de riesgos.
