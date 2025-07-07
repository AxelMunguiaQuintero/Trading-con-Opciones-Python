# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt

# Parámetros comunes
strike = 100
prima_call = 10
prima_put = 10

# Rango de precios del subyacente (vencimiento)
precios = np.linspace(50, 150, 100)

# Definir funciones de Payoff para cada posición
def call_largo(S, K, prima): return np.maximum(S - K, 0) - prima
def call_corto(S, K, prima): return -call_largo(S, K, prima)
def put_largo(S, K, prima): return np.maximum(K - S, 0) - prima
def put_corto(S, K, prima): return -put_largo(S, K, prima)
def accion_larga(S, K): return S - K
def accion_corta(S, K): return -accion_larga(S, K)

# Construcción de Posiciones Sintéticas

# 1. Acción Sintética (Larga) = Long Call + Short Put (Mismo Strike y mismo vencimiento)

# Uso:
#   - Replicar una acción cuando no se puede comprar directamente.
#   - Aprovechar un apalancamiento mayor usando margen.
#   - Evitar restricciones regulatorias o de impuestos sobre la compra directa de acciones.
accion_sintetica_larga = call_largo(S=precios, K=strike, prima=prima_call) + put_corto(S=precios, K=strike, prima=prima_put)

# 2. Acción Sintética (Corta) = Short Call + Long Put (Mismo Strike y mismo vencimiento)
# Uso:
#   - Tomar una posición bajista sin vender en corto plazo.
#   - Evitar problemas con laa disponibilidad para hacer short selling.
#   - Cobertura de portafolios cuando se espera una caída del subyacente.
accion_sintetica_corta = call_corto(S=precios, K=strike, prima=prima_call) + put_largo(S=precios, K=strike, prima=prima_put)

# 3. Long Call Sintético = Long Stock + Long Put ATM
# Uso:
#   - Cobertura ante caídas del activo (protección tipo seguro).
#   - Reproducir un call cuando no hay liquidez en el mercado de opciones.
call_sintetico = accion_larga(S=precios, K=strike) + put_largo(S=precios, K=strike, prima=prima_put)

# 4. Long Put Sintético = Short Stock + Long Call ATM
# Uso:
#   - Proteger una posición corta en el subyacente (cobertura).
#   - Simular una put cuando las puts son caras o ilíquidas.
#   - Estrategia direccional bajista con pérdida limitada.
put_sintetico = accion_corta(S=precios, K=strike) + call_largo(S=precios, K=strike, prima=prima_call)

# 5. Short Put Sintético = Short Call ATM + Long Stock
# Uso:
#   - Reproducir una put cuando no hay liquidez en puts.
#   - Estrategia alcista con capital reducido comparado con put short directa.
#   - Obtener ingresos con mayor flexibilidad usando acciones y opciones.
short_put_sintetico = call_corto(S=precios, K=strike, prima=prima_put) + accion_larga(S=precios, K=strike)

# 6. Short Call Sintético = Short Put ATM + Short Stock
# Uso:
#   - Simular la venta de una call cuaando hay limitaciones en calls.
#   - Estrategia bajista moderada con mayor control del riesgo.
#   - Cobertura parcial en portafolios largos para reducir exposición alcista
short_call_sintetico = put_corto(S=precios, K=strike, prima=prima_put) + accion_corta(S=precios, K=strike)

# Generar Plots
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(24, 10), dpi=300)
fig.suptitle("Posiciones Sintéticas con Opciones", fontsize=16, weight="bold")

# 1. Acción Sintética Larga
axs[0, 0].plot(precios, call_largo(S=precios, K=strike, prima=prima_call), "--", label="Long Call")
axs[0, 0].plot(precios, put_corto(S=precios, K=strike, prima=prima_put), "--", label="Short Put")
axs[0, 0].plot(precios, accion_sintetica_larga, label="Acción Sintética Larga", color="black")
axs[0, 0].set_title("Acción Sintética Larga = Long Call + Short Put")

# 2. Acción Sintética Corta
axs[0, 1].plot(precios, call_corto(S=precios, K=strike, prima=prima_call), "--", label="Short Call")
axs[0, 1].plot(precios, put_largo(S=precios, K=strike, prima=prima_put), "--", label="Long Put")
axs[0, 1].plot(precios, accion_sintetica_corta, label="Acción Sintética Corta", color="black")
axs[0, 1].set_title("Acción Sintética Corta = Short Call + Long Put")

# 3. Long Call Sintético
axs[0, 2].plot(precios, accion_larga(S=precios, K=strike), "--", label="Long Stock")
axs[0, 2].plot(precios, put_largo(S=precios, K=strike, prima=prima_put), "--", label="Long Put")
axs[0, 2].plot(precios, call_sintetico, label="Call Sintético", color="black")
axs[0, 2].set_title("Call Sintético = Long Stock + Long Put")

# 4. Long Put Sintético
axs[1, 0].plot(precios, accion_corta(S=precios, K=strike), "--", label="Short Stock")
axs[1, 0].plot(precios, call_largo(S=precios, K=strike, prima=prima_call), "--", label="Long Call")
axs[1, 0].plot(precios, put_sintetico, label="Put Sintético", color="black")
axs[1, 0].set_title("Put Sintético = Short Stock + Long Call")

# 5. Short Put Sintético = Short Call + Long Stock
axs[1, 1].plot(precios, call_corto(S=precios, K=strike, prima=prima_call), "--", label="Short Call")
axs[1, 1].plot(precios, accion_larga(S=precios, K=strike), "--", label="Long Stock")
axs[1, 1].plot(precios, short_put_sintetico, label="Short Put Sintético", color="black")
axs[1, 1].set_title("Short Put Sintético = Short Call + Long Stock")

# 6. Short Call Sintético = Short Put + Short Stock
axs[1, 2].plot(precios, put_corto(S=precios, K=strike, prima=prima_put), "--", label="Short Put")
axs[1, 2].plot(precios, accion_corta(S=precios, K=strike), "--", label="Short Stock")
axs[1, 2].plot(precios, short_call_sintetico, label="Short Call Sintético", color="black")
axs[1, 2].set_title("Short Call Sintético = Short Put + Short Stock")

# Agregar trazos y activar etiquetas
for ax in axs.flatten():
    ax.axhline(y=0, color="gray", lw=0.5)
    ax.legend()
    ax.grid()
    
plt.tight_layout()
plt.show()

# Recordatorio:
#   - Las posiciones sintéticas permiten replicar el comportamiento de activos o estrategias usando combinaciones
#     de opciones y subyacentes, facilitando cobertura, arbitraje, limitaciones regulatorias o acceso a estrategias
#     con menor capital inicial.
#   - Recordemos que al crear posiciones sintéticas con opciones, podría ser necesario realizar un roll over conforme 
#     se acerque el vencimiento, extendiendo así la exposición deseada y evitando asignaciones, pérdidas de cobertura
#     o desajustes en la estrategia original conforme cambian las condiciones del mercado.
