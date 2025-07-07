# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la Simulación
precio_inicial = 100
tasa_libre_riesgo = 0.05
volatilidad_anual = 0.20
horizonte_tiempo = 1
intervalos = 252
n_trayectorias = 500

# Crear el vector de tiempo
vector_tiempo = np.linspace(0, horizonte_tiempo, intervalos + 1)
dt = horizonte_tiempo / intervalos

# Inicializar la matriz de trayectorias
trayectorias_simuladas = np.zeros((n_trayectorias, intervalos + 1))
trayectorias_simuladas[:, 0] = precio_inicial

# Simulación de trayectorias usando Movimiento Browniano Geométrico:
# S(t) = S0 * exp[(mu - 0.5 * sigma**2) * t + sigma * W(t)],
# donde W(t) ≈ ε * sqrt(t), siendo ε una variable aleatoria normal estándar N(0, 1)

np.random.seed(42) # Para reproducibilidad
for i in range(n_trayectorias): 
    for t in range(1, intervalos + 1):
        # Definir W(t)
        w_t = np.random.normal(loc=0, scale=1) * np.sqrt(dt)
        # Simular Nuevo Precio para la trayectoria actual
        trayectorias_simuladas[i, t] = trayectorias_simuladas[i, t - 1] * np.exp((tasa_libre_riesgo - 0.5 * volatilidad_anual ** 2) * dt + \
                                                                                 volatilidad_anual * w_t)
            
# Estadísticas de las trayectorias
precios_finales = trayectorias_simuladas[:, -1] # Precios finales de todas las trayectorias
maximos_precios = np.max(trayectorias_simuladas, axis=1) # Máximos precios alcanzados en cada trayectoria
minimos_precios = np.min(trayectorias_simuladas, axis=1) # Mínimos precios alcanzados en cada trayectoria

# Cálculo de Percentiles
percentil_1 = np.percentile(precios_finales, 1) # Peor Escenario (1% más bajo con peores precios)
percentil_99 = np.percentile(precios_finales, 99) # Mejor Escenario (1% más alto con mejores precios)

# Promedio de los precios finales
promedio_final = np.mean(precios_finales)

# Desviación Estándar de los precios finales
desviacion_estandar = np.std(precios_finales)

# Mostrar estadísticas de riesgo y oportunidad
print("Estadísticas de las Trayectorias Simuladas (Riesgo y Oportunidad):")
print(f"Promedio de los Precios Finales: {promedio_final:.2f}")
print(f"Peor Escenario (Percentil 1%): {percentil_1:.2f}")
print(f"Mejor Escenario (Percentil 99%): {percentil_99:.2f}")
print(f"Desviación Estándar de los precios finales: {desviacion_estandar:.2f}")
print(f"Precio máximo alcanzado en una trayectoria: {np.max(maximos_precios):.2f}")
print(f"Precio mínimo alcanzado en una trayectoria: {np.min(minimos_precios):.2f}")

# Visualización de las trayectorias y estadísticas
plt.figure(figsize=(22, 6), dpi=300)

# Trayectorias Simuladas
for i in range(trayectorias_simuladas.shape[0]):
    plt.plot(vector_tiempo, trayectorias_simuladas[i])
    
# Línea de los precios promedio
plt.plot(vector_tiempo, np.mean(trayectorias_simuladas, axis=0), color="black", linestyle="--", label="Precio Promedio")

# Agregar líneas para los precios máximos y mínimos globales
plt.axhline(y=np.max(maximos_precios), color="red", linestyle="--", label="Precio Máximo Global")
plt.axhline(y=np.min(minimos_precios), color="blue", linestyle="--", label="Precio Mínimo Global")

# Agregar líneas para los percentiles de riesgo y oportunidad
plt.axhline(y=percentil_1, color="orange", linestyle=":", label=f"Peor Escenario (1%): {percentil_1:.2f}")
plt.axhline(y=percentil_99, color="green", linestyle=":", label=f"Mejor Escenario (99%): {percentil_99:.2f}")

plt.title("Simulación Monte Carlo: Generación de Trayectorias de Precios con Riesgo y Oportunidad")
plt.xlabel("Tiempo (años)")
plt.ylabel("Precio del Activo")
plt.grid()
plt.legend()
plt.show()

# Recordatorio:
#   - La Simulación Monte Carlo permite modelar cientos de trayectorias posibles del precio, capturando
#     comportamientos futuros bajo incertidumbre y ayudando a anticipar riesgos y oportunidades en inversiones.
