# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
from scipy.stats import norm

# Conocer la Función de Aproximación Delta-Gamma-Theta-Vega:
    
# Letras Griegas en Unicode
delta = chr(0x0394)
gamma = chr(0x0393)
theta = chr(0x0398)
sigma = chr(0x03C3)

# Otros símbolos matemáticos en Unicode
approx = chr(0x2248)
times = chr(0x00D7)
half = chr(0x00BD)
squared = chr(0x00B2)

# Construir ecuación usando caracteres unicode
formula = (
    
    f"{delta}V {approx} {delta} {times} {delta}S + {half} {times} {gamma} {times} "
    f"({delta}S){squared} + {theta} {times} {delta}t + Vega {times} {delta}{sigma}"
    
    )

print(formula)

# Definir función de Black-Scholes
def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    
    """
    Función que obtiene el valor de la prima de una opción europea.
    """
    
    # Calcular
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    prima = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2) if option_type == "call" else \
        K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
    return prima

# Definir una función para calcular las griegas
def calcular_griegas(S, K, T, r, sigma, option_type="call"):
    
    """
    Calcula Delta, Gamma, Theta y Vega para una opción europea.
    """
    
    # Calcular
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # Obtener Delta y Theta
    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    elif option_type == "put":
        delta = norm.cdf(d1) - 1
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    else:
        raise ValueError("El tipo de opción debe ser 'call' o 'put'")
    # Obtener Gamma y Vega
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    
    return delta, gamma, theta, vega

# Definir Función de Aproximación
def delta_gamma_theta_vega_aprox(S, K, T, r, sigma, delta_S, delta_t, delta_sigma, option_type="call"):
    
    """
    Aproximación del cambio en el valor usando Delta-Gamma-Theta-Vega.
    """
        
    # Calcular el precio de la prima
    precio_original = black_scholes_price(S, K, T, r, sigma, option_type)
    # Obtener Griegas
    delta, gamma, theta, vega = calcular_griegas(S, K, T, r, sigma, option_type)
    # Calcular cambio (utilizando la función)
    cambio_valor = (delta * delta_S + 0.5 * gamma * (delta_S ** 2) + theta * delta_t + vega * delta_sigma)
    precio_aproximacion = precio_original + cambio_valor
    
    return precio_aproximacion, precio_original, cambio_valor, (delta, gamma, theta, vega)

# Parámetros Iniciales
S = 100
K = 100
T = 0.25
r = 0.05
sigma = 0.20

# Cambios Esperados
delta_S = 2    # Cambio en el subyacente (Incremento es Positivo y Decremento Negativo)
delta_t = 1    # Cambio temporal (1 día Menos)  
delta_sigma = -5 # Cambio en volatilidad implícita (Disminuye 5%)

# Simulación Call y Put
tipos_opcion = ["call", "put"]
resultados = {}
for tipo in tipos_opcion:
    aprox, orig, cambio, griegas = delta_gamma_theta_vega_aprox(S, K, T, r, sigma, delta_S, delta_t, delta_sigma, option_type=tipo)
    resultados[tipo] = {
        "aprox": aprox,
        "orig": orig,
        "cambio": cambio,
        "delta": griegas[0],
        "gamma": griegas[1],
        "theta": griegas[2],
        "vega": griegas[3]        
        }

# Mostrar Resultados
for tipo in tipos_opcion:
    res = resultados[tipo]
    print(f"""
    Aproximación Delta-Gamma-Theta-Vega: {tipo}
          
    Precio Original: ${res['orig']:.2f}
    Precio Estimado ({delta}{gamma}{theta}V): ${res['aprox']:.2f}
    Cambio Estimado: ${res['cambio']:.2f}
    
    Griegas:         
    Delta: {res['delta']:6f}
    Gamma: {res['gamma']:6f}
    Theta: {res['theta']:6f}
    Vega (por punto %): {res['vega']:6f}    
          """)
    
# Recordatorio:
#   - La Función de Aproximación DGTV permite estimar rápidamente cómo varía el precio de una opción ante pequeños
#     cambios en el precio del subyacente, volatilidad y tiempo, sin recalcular el modelo completo de Black-Scholes.
#   - También facilita la toma de decisiones informadas en trading, simulando escenarios futuros y evaluando pérdidas
#     o ganancias esperadas, especialmente útil para ajustar, cubrir o cerrar posiciones con opciones.
