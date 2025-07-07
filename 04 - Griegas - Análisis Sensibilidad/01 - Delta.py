# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import scipy.stats as si
from datetime import datetime
import matplotlib.pyplot as plt

# Indicar una breve explicación de Delta
print("""
La Delta es una de las principales griegas de las opciones financieras.
Representa la sensibilidad del precio de una de una opción con respecto al precio del activo subyacente.

Es decir, nos indica cuánto cambia el valor de una opción si el precio del activo subyacente cambia en 1 unidad.

- Para una Call: Delta está en el intervalo (0, 1)
- Para un Put: Delta está en el intervalo (-1, 0)

Interpretación básica:
- Una Delta de 0.5 en un call implica que si el subyacente sube 1 USD, la opción sube 0.5 USD.
- En una estrategia de cobertura (delta hedging), se usa para neutralizar el riesgo direccional.
""")

# Definir una función para calcular Delta
def black_scholes_delta(S, K, T, r, sigma, q=0, tipo="call"):
    
    """
    Calcula la delta de una opción utilizando el modelo de BSM.
    """
    
    # Calcular Delta
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    if tipo == "call":
        return si.norm.cdf(d1)
    elif tipo == "put":
        return si.norm.cdf(d1) - 1
    else:
        raise ValueError("El tipo debe ser 'call' o 'put'")
        
# Ejemplo rápido
S = 100
K = 105
T = 0.5
r = 0.05
sigma = 0.25
delta_call = black_scholes_delta(S, K, T, r, sigma, q=0, tipo="call")
delta_put = black_scholes_delta(S, K, T, r, sigma, q=0, tipo="put")
print(f"Valor Delta para Call: {delta_call}")
print(f"Valor Delta para Put: {delta_put}")
print(delta_call + delta_put * -1)
        
# Visualizar Delta para distintos niveles de Precios
def graficar_delta(S_min=50, S_max=150, K=100, T=0.5, r=0.05, sigma=0.25):
    
    """
    Graficar la delta de una call y una put respecto al precio del subyacente.
    """
    
    # Calcular diferentes Deltas
    precios = np.linspace(start=S_min, stop=S_max, num=200)
    delta_calls = [black_scholes_delta(S, K, T, r, sigma, q=0, tipo="call") for S in precios]
    delta_puts = [black_scholes_delta(S, K, T, r, sigma, q=0, tipo="put") for S in precios]
    # Graficar
    plt.figure(figsize=(22, 10), dpi=300)
    plt.plot(precios, delta_calls, label="Delta Call", color="blue")
    plt.plot(precios, delta_puts, label="Delta Put", color="red")
    plt.axvline(K, color="gray", linestyle="--", label="Precio Strike (K)")
    plt.title("Delta de Opciones vs Precio del Subyacente")
    plt.xlabel("Precio del Subyacente (S)")
    plt.ylabel("Delta")
    plt.legend()
    plt.grid()
    plt.show()
    
# Ejecutar la visualización
graficar_delta()

# Visualizar la Griega Delta para Datos Reales
ticker = "SPY"
activo = yf.Ticker(ticker=ticker)
fechas_disponibles = activo.options
fecha_objetivo = fechas_disponibles[15]
tiempo_restante = (pd.to_datetime(fecha_objetivo) - datetime.now()).days / 365
cadena_opciones = activo.option_chain(date=fecha_objetivo)
calls, puts, underlying_info = cadena_opciones
precio_spot = underlying_info["regularMarketPrice"]
# Calcular Delta real para cada opción dentro de la cadena de opciones
calls["Delta"] = calls.apply(lambda x: black_scholes_delta(S=precio_spot, K=x["strike"], T=tiempo_restante, 
                                                           r=0.05, sigma=x["impliedVolatility"], q=0, tipo="call"),
                             axis=1)
puts["Delta"] = puts.apply(lambda x: black_scholes_delta(S=precio_spot, K=x["strike"], T=tiempo_restante, 
                                                           r=0.05, sigma=x["impliedVolatility"], q=0, tipo="put"),
                             axis=1)

# Gráfico: Delta vs Strike
plt.figure(figsize=(22, 6), dpi=300)
plt.scatter(calls["strike"], calls["Delta"], color="blue", label="Delta Call (Real)", alpha=0.7)
plt.scatter(puts["strike"], puts["Delta"], color="red", label="Delta Put (Real)", alpha=0.7)
plt.axvline(x=precio_spot, color="black", linestyle="--", label="Precio Subyacente (Spot)")
plt.title(f"Delta de Opciones Reales ({ticker}) con vencimiento en {fecha_objetivo}")
plt.xlabel("Precio de Ejercicio (Strike)")
plt.ylabel("Delta")
plt.grid()
plt.legend()
plt.show()

# Delta vs Subyacente (con Strike fijo usando datos reales)

# Elegir opción representativa (strike más cercano al spot)
idx_strike_cercano = (calls["strike"] - precio_spot).abs().argmin()
strike_representativo = calls.iloc[idx_strike_cercano]["strike"]
iv_representativa = calls.iloc[idx_strike_cercano]["impliedVolatility"]

# Rango de precios del subyacente
rango_S = np.linspace(precio_spot * 0.80, precio_spot * 1.20, num=200)

# Calcular Delta usando parámetros reales pero variando S
deltas_call_real = [black_scholes_delta(S=S, K=strike_representativo, T=tiempo_restante, 
                                        r=0.05, sigma=iv_representativa, q=0, tipo="call") for S in rango_S]
deltas_put_real = [black_scholes_delta(S=S, K=strike_representativo, T=tiempo_restante, 
                                        r=0.05, sigma=puts[puts["strike"]==strike_representativo]["impliedVolatility"].iloc[0],
                                        q=0, tipo="put") for S in rango_S]

# Gráfico: Delta vs Precio del Subyacente (Real)
plt.figure(figsize=(22, 6))
plt.plot(rango_S, deltas_call_real, label="Delta Call (Real, Strike Fijo)", color="blue")
plt.plot(rango_S, deltas_put_real, label="Delta Put (Real, Strike Fijo)", color="red")
plt.axvline(x=strike_representativo, color="gray", linestyle="--", label=f"Strike Fijo: {strike_representativo:.2f}")
plt.title(f"Delta de Opciones Reales ({ticker}) vs Precio del Subyacente (Strike Fijo)")
plt.xlabel("Precio del Subyacente (S)")
plt.ylabel("Delta")
plt.grid()
plt.legend()
plt.show()

# Análisis adicional del comportamiento
def analisis_comportamiento():
    
    """
    Analiza cómo varía la Delta con diferentes parámetros: tiempo y volatilidad.
    """
    
    # Definir parámetros
    K = 100
    r = 0.05
    precios = np.linspace(start=50, stop=150, num=200)
    volatidades = [0.10, 0.30, 0.60]
    tiempos = [0.05, 0.5, 1.0]
    
    # Crear Gráfico
    plt.figure(figsize=(22, 6), dpi=300)
    
    for i, sigma in enumerate(volatidades):
        plt.subplot(1, 3, i + 1)
        for T in tiempos:
            # Obtener Deltas variando los parámetros
            deltas = [black_scholes_delta(S=S_actual, K=K, T=T, r=r, sigma=sigma, q=0, tipo="call")
                      for S_actual in precios]
            plt.plot(precios, deltas, label=f"T={T:.2f} años")
        # Agregar detalles al gráfico
        plt.title(f"Delta Call con Volatilidad = {sigma}")
        plt.ylabel("Delta")
        plt.xlabel("Precio del Subyacente (S)")
        plt.ylim(-0.1, 1.1)
        plt.legend()
        plt.grid()
    
    plt.tight_layout()
    plt.show()

    
# Ejecutar análisis
analisis_comportamiento()

# Aplicación Práctica: Delta Hedging
print("""
Cobertura Delta (Delta Hedging)

¿Qué es?
La Cobertura delta es una estrategia que se usa para eliminar o reducir el riesgo relacionado con los movimientos
del precio del activo subyacente en una posición de opciones. La Delta nos indica cuánto cambie el precio de una
opción cuando cambia el precio del activo, por lo que podemos usarla para crear una cartera 'neutral' que no se vea
afectada por pequeñas variaciones en el precio del activo.

¿Cómo funciona en la práctica?
Imagina que vendes 1 contrato de opciones call europeas (que equivalen a 100 acciones). Al vender calls, tienes una
posición que pierde valor si el precio del activo sube. Para protegerte, puedes comprar acciones del activo en la
cantidad que corresponde a la Delta de esas opciones.

¿Por qué esta estrategia es efectiva?
- Si el precio del activo sube, la opción call se encarece (tú pierdes como vendedor), pero las acciones que compraste
  ganan valor, compensando esa pérdida.
- Si el precio baja, la opción pierde valor (tú ganas), pero las acciones pierden valor, equilibrando la ganancia.

Lo importante es que esta cobertura debe ajustarse constantemente porque la Delta cambia con el tiempo y con el 
precio del activo, para mantener la neutralidad del riesgo.      
""")

def ejemplo_cobertura_delta():
    
    """
    Simula una cobertura delta simple en un punto del tiempo.
    """

    # Definir parámetros iniciales
    S = 105
    K = 100
    T = 0.25
    r = 0.05
    sigma = 0.20
    
    # Calcular la deltaa del Call (Siempre Positiva)
    delta_call = black_scholes_delta(S, K, T, r, sigma, tipo="call")
    print(f"Delta de la Call: {delta_call:.4f}")
    
    # Supón que vendemos 1 contrato de calls (posición corta)
    acciones_x_contrato = 100
    delta_posicion_corta = -delta_call * acciones_x_contrato # Negativo porque la posición es corta
    
    print(f"Delta neta de la posición corta en calls: {delta_posicion_corta:.2f}")
    
    # Para cubrir esta posición, compramos acciones en cantidad igual a la Delta absoluta (Postivo)
    acciones_cobertura = abs(delta_posicion_corta)
    print(f"\nPara cubrir esta posición, deberías comprar aproximadamente {acciones_cobertura:.2f} acciones del subyacente")

# Ejecutar el ejemplo de cobertura
ejemplo_cobertura_delta()

# Recordatorio:
#   - La Cobertura delta neutral no es para "hacer que tu cartera nunca cambie", sino para protegerte contra el riesgo
#     de movimiento del precio del activo y permite enfocarte en ganar con los cambios en la volatilidad, el tiempo
#     y otros factores. Así, puedes capturar ganancias consistentes y controladas, minimizando pérdidas inesperadas
#     por subidas o bajadas bruscas del activo subyacente.
