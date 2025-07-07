# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt

# Configuración del entorno de simulación (Parámetros del Activo)
S0 = 100          # Precio Inicial del Activo
mu = 0.10         # Rendimiento Anual Esperado (10%)
sigma = 0.2       # Volatilidad Anual (20%)
n_pasos = 252     # Número de pasos de simulación (usamos 252 días hábiles, típico del mercado financiero)
T = 1.0           # Horizonte Temporal total de la simulación (1 año)
dt = T / n_pasos  # Tamaño del intervalo temporal entre pasos
n_trayectorias= 5 # Cantidad de trayectorias (simulaciones) que se desean generar

# Ecuación del Movimiento Browniano Geométrico:
# S(t) = S0 * exp[(mu - 0.5 * sigma^2) * t + sigma * W(t)]
# donde W(t) es una realización del proceso de Wiener (Movimiento Browniano estándar), es decir,
# W(t) = sqrt(t) * ε, con ε ~ N(0, 1)

# Crear vector de tiempo para la simulación
t = np.linspace(start=0, stop=T, num=n_pasos + 1)

# Inicializar matriz para almacenar las trayectorias simuladas
gbm_paths = np.zeros((n_trayectorias, n_pasos + 1))

for i in range(n_trayectorias):
    # Generar incrementos normales independientes para el proceso de Wiener
    W_increments = np.random.normal(loc=0, scale=np.sqrt(dt), size=n_pasos)
    # Calcular la trayectoria del proceso de Wiener como una suma acumulada de los incrementos
    W_cumsum = np.cumsum(W_increments)
    # Insertar el valor inicial 0 para W(0)
    W_cumsum = np.insert(W_cumsum, 0, 0)
    
    # Calcular la trayectoria del precio según la fórmula del GBM
    gbm_paths[i] = S0 * np.exp((mu - 0.5 * sigma ** 2) * t + sigma * W_cumsum)
    
# Graficar las trayectorias simuladas
plt.figure(figsize=(22, 8))
for i in range(n_trayectorias):
    plt.plot(t, gbm_paths[i], label=f"Tractoria {i+1}")
plt.title("Simulación del Movimiento Browniano Geométrico (5 trayectorias del precio)")
plt.xlabel("Tiempo (años)")
plt.ylabel("Precio del Activo S(t)")
plt.grid()
plt.legend()
plt.show()

# Recordatorio:
#   - El Movimiento Browniano Geométrico asegura que los precios se mantengan positivos y reflejan un crecimiento compuesto con
#     volatilidad.
#   - La volatilidad mide la intensidad de las fluctuaciones aleatorias del precio.
#   - El rendimiento esperado representa la tendencia promedio de crecimiento anual del activo.
#   - Simular múltiples trayectorias nos ayuda a visualizar la incertidumbre inherente y posibles caminos futuros del precios,
#     útiles para análisis y toma de decisiones financieras.
