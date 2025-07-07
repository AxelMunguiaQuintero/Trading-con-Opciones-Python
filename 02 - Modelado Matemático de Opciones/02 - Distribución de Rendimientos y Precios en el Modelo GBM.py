# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de parámetros para la simulación
mu = 0.08
sigma = 0.20
S0 = 100
T = 1
n_sims = 1_000
n_steps = 252
dt = T / n_steps

# Distribución Normal (Teórica) vs. Rendimientos Simulados

# Definir la media y la varianza de los rendimientos
mu_r = (mu - 0.5 * sigma ** 2) * dt
sigma_r = sigma * np.sqrt(dt)

# Generar distribución normal teórica
distr_normal = np.random.normal(loc=mu_r, scale=sigma_r, size=(n_sims * n_steps))

# Simular rendimientos logarítmicos diarios (MBG):
# Ecuación del Movimiento Browniano Geométrico: S(t) = S0 * exp[(mu - 0.5 * sigma**2) * t + sigma * W(t)]
# Aplicar Logaritmos a la Ecuación MBG: ln(S_t / S_0) = (mu - 0.5 * sigma**2) * t + sigma * W(t)

# Donde W(t) es un proceso de Wiener (Movimiento Browniano estándar), que puede simularse en pasos
# discretos como W(t) ≈ ε * sqrt(t), siendo ε una variable aleatoria normal estándar N(0,1).

# Opción 1: Crear Precios y Después obtener los Rendimientos

# Vector de tiempo para la simulación
t = np.linspace(start=0, stop=T, num=n_steps + 1)
# Incrementos de Wiener para cada simulación
dW = np.random.normal(loc=0.0, scale=np.sqrt(dt), size=(n_sims, n_steps))
# Proceso de Wiener Acumulado (Insertar también 0 en la primera posición)
W = np.concatenate([np.zeros((n_sims, 1)), np.cumsum(dW, axis=1)], axis=1)
# Precios Simulados
precios = S0 * np.exp((mu - 0.5 * sigma ** 2) * t + sigma * W)
# Calcular rendimientos logarítmicos diarios
rend_log = np.log(precios[:, 1:] / precios[:, :-1]).ravel()

# Opción 2: Generar los Rendimientos con la fórmula despejada
rend_directos = (mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.normal(loc=0.0, scale=1, size=(n_sims * n_steps))

# Graficar y Comparar Comportamientos
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(22, 6), dpi=300)

# 1. Distribución normal teórica
sns.histplot(distr_normal, bins=50, kde=True, color="blue", ax=axes[0])
axes[0].set_title("Distribución Normal Teórica")
axes[0].set_xlabel("Rendimientos logarítmicos diarios")
axes[0].set_ylabel("Frecuencia")

# 2. Rendimientos logarítmicos simulados (Opción 1)
sns.histplot(rend_log, bins=50, kde=True, color="green", ax=axes[1])
axes[1].set_title("Rendimientos logarítmicos simulados (MBG)")
axes[1].set_xlabel("Rendimientos logarítmicos diarios")
axes[1].set_ylabel("Frecuencia")

# 3. Rendimientos generados directamente (Opción 2)
sns.histplot(rend_directos, bins=50, kde=True, color="red", ax=axes[2])
axes[2].set_title("Rendimientos Generados Directamente")
axes[2].set_xlabel("Rendimientos logarítmicos diarios")
axes[2].set_ylabel("Frecuencia")

plt.tight_layout()
plt.show()

# Distribución Lognormal (Teórica) vs. Precios Simulados

# Generar distribución lognormal con parámetros del activo
mu_log = np.log(S0) + (mu - 0.5 * sigma**2) * T
sigma_log = sigma * np.sqrt(T)
lognormal_teorica = np.random.lognormal(mean=mu_log, sigma=sigma_log, size=n_sims * 10)

# Simular 10_000 distintos trayectorias de Precios:
precios_finales_directos = S0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * np.random.randn(n_sims * 10))

# Graficar distribución lognormal vs Precios Simulados
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(22, 6), dpi=300)

# Histograma distribución lognormal teórica
sns.histplot(lognormal_teorica, bins=50, kde=True, color="purple", label="Lognormal", ax=ax[0])
ax[0].set_title("Distribución Lognormal Teórica")
ax[0].set_xlabel("Precios")
ax[0].set_ylabel("Frecuencia")
ax[0].legend()

# Histograma precios finales simulados (MBG)
sns.histplot(precios_finales_directos, bins=50, kde=True, color="orange", label="Precios Finales Simulados", ax=ax[1])
ax[1].set_title("Distribución de Precios Simulados (MBG)")
ax[1].set_xlabel("Precios")
ax[1].set_ylabel("Frecuencia")
ax[1].legend()

plt.tight_layout()
plt.show()

# Recordatorio:
#   - Los rendimientos logarítmicos simulados a partir del Movimiento Browniano Geométrico presentan una forma
#     simétric tipo campana, confirmando que siguen una distribución normal, como asume la teoría.
#   - Al comparar los precios simulados con una distribución lognormal teórica, observamos asimetría positiva,
#     validando que los precios bajo el MBG no son normales, sino lognormales, como predice el modelo.
