# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Indicar un resumen de Theta
print("""
Theta mide la sensibilidad del precio de una opción respecto al paso del tiempo.

Es decir, indica cuánto pierde (o gana) de valor una opción por el simple hecho de que el tiempo pasa,
manteniendo todo lo demás constante.

En general:
    - Las opciones pierden valor con el tiempo -> Theta negativo
    - Los vendedores de opciones 'ganan' este valor -> les beneficia
    - El efecto se acelera cuando el tiempo a vencimiento es bajo

Theta también se conoce como 'decadencia temporal'      
""")

# Definir función para calcular Theta
def calcular_theta(S, K, T, r, sigma, tipo_opcion):
    
    """
    Calcula a Theta para una opción europea.
    """
    
    # Obtener valores auxiliares
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    # Validar el Tipo de Opción
    if tipo_opcion.lower() == "call":
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2))
    elif tipo_opcion.lower() == "put":
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2))
    else:
        raise ValueError("El tipo de opción debe ser 'call' o 'put'")
        
    return theta / 365 # Theta por día

# Parámetros Generales
S = 100
K = 100
T = 0.5
r = 0.05
sigma = 0.25
call_theta_valor = calcular_theta(S, K, T, r, sigma, tipo_opcion="call")
put_theta_valor = calcular_theta(S, K, T, r, sigma, tipo_opcion="put")

# Desplegar Valores
print("Theta Call:", call_theta_valor)
print("Theta Put:", put_theta_valor)

# Generar visualización con Theta
def graficar_Theta(S_min = 50, S_max = 150, K = 100, T=0.5, r=0.05, sigma = 0.25):
    
    """
    Grafica la Theta de una opción call y put respecto al precio del subyacente.
    """

    # Calcular Theta
    precios = np.linspace(S_min, S_max, 200)
    thetas_call = [calcular_theta(S, K, T, r, sigma, tipo_opcion="call") for S in precios]
    thetas_put = [calcular_theta(S, K, T, r, sigma, tipo_opcion="put") for S in precios]
    # Graficar
    plt.figure(figsize=(22, 6), dpi=300)
    plt.plot(precios, thetas_call, label=f"Theta Call (T={T*365:.1f} días)", color="brown")
    plt.plot(precios, thetas_put, label=f"Theta Put (T={T*365:.1f} días)", color="blue")
    plt.axhline(y=0, color="gray", linestyle="--")
    plt.axvline(K, color="gray", linestyle="--", label="Precio Strike")
    plt.title("Theta de Opciones Call y Put vs Precio del Subyacente")
    plt.xlabel("Precio del Subyacente")
    plt.ylabel("Theta (Valor Perdido por día)")
    plt.legend()
    plt.grid()
    plt.show()
    
# Correr Función
graficar_Theta()

# Visualizar Theta con múltiples vencimientos
def graficar_theta_multiples_vencimientos(S_min=35, S_max=65, K=50, r=0.05, sigma=0.25):
    
    """
    Grafica Theta para opciones Call y Put.
    """
    
    # Definir parámetros
    vencimientos_dias = [7, 30, 60]
    precios = np.linspace(start=S_min, stop=S_max, num=300)
    colores = ["magenta", "green", "blue"]
    
    # Generar Plot
    fig, axs = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    # Iterar en Parámetros
    for i, T_dias in enumerate(vencimientos_dias):
        T = T_dias / 365
        thetas_call = [calcular_theta(S, K, T, r, sigma, tipo_opcion="call") for S in precios]
        thetas_put = [calcular_theta(S, K, T, r, sigma, tipo_opcion="put") for S in precios]
        axs[0].plot(precios, thetas_call, label=f"{T_dias} días", color=colores[i])
        axs[1].plot(precios, thetas_put, label=f"{T_dias} días", color=colores[i])
        
    # Configuración subplot Call
    axs[0].axvline(K, color="gray", linestyle="--", label="Precio Strike")
    axs[0].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axs[0].set_title("Theta Call vs Precios del Subyacente")
    axs[0].set_xlabel("Precio del Subyacente")
    axs[0].set_ylabel("Theta")
    axs[0].legend()
    axs[0].grid()
    
    # Configuración subplot Put
    axs[1].axvline(K, color="gray", linestyle="--", label="Precio Strike")
    axs[1].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axs[1].set_title("Theta Put vs Precios del Subyacente")
    axs[1].set_xlabel("Precio del Subyacente")
    axs[1].set_ylabel("Theta")
    axs[1].legend()
    axs[1].grid()

    plt.suptitle("Theta para Opciones Call y Put con distintos tiempos a vencimiento")
    plt.tight_layout()
    plt.show()
    
# Ejecutar función
graficar_theta_multiples_vencimientos()

# Observar la pérdida de valor de una opción
def simular_decay_calls_y_puts():
    
    """
    Simula la decadencia temporal de opciones call y put en subplots.
    """

    # Parámetros comunes
    S = 100
    K = 100
    r = 0.05
    sigma = 0.25
    dias = np.arange(1, 366)
    
    # Lista para almacenar valores
    precios_call = []
    precios_put = []
    
    # Calcular precios diariamente
    for d in dias:
        T = d / 365
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        precios_call.append(call_price)
        precios_put.append(put_price)

    # Crear figura
    fig, axs = plt.subplots(1, 2, figsize=(20, 10), dpi=200)
    
    # Subplot Call
    axs[0].plot(dias, precios_call, label="Precio Call", color="brown")
    axs[0].set_title("Decadencia Temporal: Opción Call")
    axs[0].set_xlabel("Días al vencimiento")
    axs[0].set_ylabel("Precio de la Call")
    axs[0].invert_xaxis()
    axs[0].grid()
    axs[0].legend()
    
    # Subplot Put
    axs[1].plot(dias, precios_put, label="Precio Put", color="teal")
    axs[1].set_title("Decadencia Temporal: Opción Put")
    axs[1].set_xlabel("Días al vencimiento")
    axs[1].set_ylabel("Precio del Put")
    axs[1].invert_xaxis()
    axs[1].grid()
    axs[1].legend()
    
    # Anotar valores cada mes aproximadamente (cada 30 días)
    for i in range(0, 13):
        idx = -(1 + i * 30)
        dias_restantes = dias[idx]
        
        # Valores actuales
        valor_call = precios_call[idx]
        valor_put = precios_put[idx]
        
        # Porcentaje de pérdida respecto al valor inicial
        perdida_call = (1 - valor_call / precios_call[-1]) * 100  # Valor correspondiente a cada mes
        perdida_put = (1 - valor_put / precios_put[-1]) * 100     # Valor correspondiente a cada mes
        
        # Anotar en el gráfico
        axs[0].annotate(f"-{perdida_call:.1f}%",
                        xy=(dias_restantes, valor_call),
                        xytext=(dias_restantes - 3, valor_call + 0.4),
                        ha="center", color="black", fontsize=9,
                        arrowprops=dict(arrowstyle="->", color="gray", lw=0.5))
        
        axs[1].annotate(f"-{perdida_put:.1f}%",
                        xy=(dias_restantes, valor_put),
                        xytext=(dias_restantes - 3, valor_put + 0.4),
                        ha="center", color="black", fontsize=9,
                        arrowprops=dict(arrowstyle="->", color="gray", lw=0.5))
        
    plt.suptitle("Comparación de la Decadencia Temporal en Opciones Europeas", fontsize=16)
    plt.tight_layout()
    plt.show()
    
# Ejecutar la simulación
simular_decay_calls_y_puts()
        
# Recordatorio:
#   - Theta nos ayuda a entender cómo el simple paso del tiempo puede destruir valor.
#   - Toda opción tiene un reloj interno que consume su valor si no hay movimiento.
#   - Dominar Theta permite diseñar estrategias más sólidas.
