# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np

# Parámetros de la Opción
precio_inicial = 100
precio_ejercicio = 100
tasa_riesgo = 0.05
volatilidad = 0.20
tiempo_madurez = 1
simulaciones = 100_000

# Simular los precios al vencimiento (S(T))
W_t = np.random.normal(loc=0, scale=1, size=simulaciones) * np.sqrt(tiempo_madurez) # Movimiento Browniano
S_T = precio_inicial * np.exp((tasa_riesgo - 0.5 * volatilidad ** 2) * tiempo_madurez + volatilidad * W_t)

# Calcular el payoff de la opción call: max(S_T - K, 0)
payoff = np.maximum(S_T - precio_ejercicio, 0)

# Descontar el promedio del payoff al valor presente
precio_opcion_call = np.exp(-tasa_riesgo * tiempo_madurez) * np.mean(payoff)

print(f"Precio Estimado de la opción Call (Monte Carlo): {precio_opcion_call:.4f}") # Precio Teórico real $10.45

# Recordatorio:
#   - La Simulación Monte Carlo permite estimar el precio justo de una prima de opción generando múltiples
#     trayectorias de precios futuros y promediando los beneficios descontados al valor presente.
