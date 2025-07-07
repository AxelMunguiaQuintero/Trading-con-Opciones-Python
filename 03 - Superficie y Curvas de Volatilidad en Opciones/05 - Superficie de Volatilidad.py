# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Leer Datos de Opciones
opciones_mercado = pd.read_csv("../datos/opciones.csv")
# Seleccionar y Ordenar las Fechas de Vencimiento
fechas_disponibles = opciones_mercado["Expiration"].unique()
fechas_disponibles = sorted(fechas_disponibles.tolist())

# Obtener el precio más reciente
ticker = "SPY"
precio_mercado = yf.Ticker(ticker=ticker).history(period="1d")["Close"].iloc[0]

# Superficie de Volatilidad (Strike vs Expiración vs IV)

# La Superficie de Volatilidad (volatility surface) es una representación tridimensional que muestra cómo
# varía la volatilidad implícita de las opciones en función de dos variables clave:
#   1. Strike (precio de ejercicio)
#   2. Tiempo a vencimiento

# Agregar días restantes al vencimiento
opciones_mercado["daysToExp"] = (pd.to_datetime(opciones_mercado["Expiration"]) - datetime.now()).dt.days + 1

# Separar Calls y Puts
calls = opciones_mercado[opciones_mercado["Type"] == "call"]
puts = opciones_mercado[opciones_mercado["Type"] == "put"]

# Crear Tablas Pivotes
surface_call = calls[["daysToExp", "strike", "impliedVolatility"]].pivot_table(values="impliedVolatility", index="strike", 
                                                                               columns="daysToExp").dropna()
surface_put = puts[["daysToExp", "strike", "impliedVolatility"]].pivot_table(values="impliedVolatility", index="strike", 
                                                                               columns="daysToExp").dropna()

# Vectores 1D
x = np.array([1, 2, 3])
y = np.array([10, 20])

# Crear mallas
X, Y = np.meshgrid(x, y)

print("Vector x:", x)
print("Vector y:", y)
print("\nMalla X:\n", X)
print("\nMalla Y:\n", Y)

# Crear mallas para las tablas pivotes
def crear_mallas(df):
    
    """
    Genera las mallas X, Y y Z necesarias para graficar una superficie 3D a partir de un DataFrame que contiene
    la volatilidad implícita de opciones.
    """
    
    X, Y = np.meshgrid(df.columns, df.index)
    Z = df.values
    
    return X, Y, Z

# Crear mallas para calls y puts
Xc, Yc, Zc = crear_mallas(surface_call)
Xp, Yp, Zp = crear_mallas(surface_put)

# Crear figura para visualizar la superficie desde distintos ángulos
fig = plt.figure(figsize=(22, 12), dpi=300)
elevs = [30, 20, 20, 30] # Elevaciones
azims = [60, 60, 120, 300] # Ángulos Horizontales

# Superficie Calls
for i in range(4):
    # Agregar cada subplot en la iteración (nrows=2, ncols=4, indice=i+1)
    ax = fig.add_subplot(2, 4, i + 1, projection="3d")
    ax.plot_surface(Xc, Yc, Zc, cmap="viridis", alpha=0.8)
    ax.set_title(f"Calls - Vista {i + 1}")
    ax.set_xlabel("Tiempo (índice)")
    ax.set_ylabel("Strike")
    ax.set_zlabel("Vol Implícita")
    ax.view_init(elev=elevs[i], azim=azims[i])
    
# Superficie Puts
for i in range(4):
    # Agregar cada subplot en la iteración (nrows=2, ncols=4, indice=i+5)
    ax = fig.add_subplot(2, 4, i + 5, projection="3d")
    ax.plot_surface(Xp, Yp, Zp, cmap="plasma", alpha=0.8)
    ax.set_title(f"Puts - Vista {i + 1}")
    ax.set_xlabel("Tiempo (índice)")
    ax.set_ylabel("Strike")
    ax.set_zlabel("Vol Implícita")
    ax.view_init(elev=elevs[i], azim=azims[i])
    
plt.suptitle("Superficie de Volatilidad Implícita - Calls y Puts desde Distintos Ángulos\n\n", fontsize=16)
plt.tight_layout()
plt.show()
    
# Recordatorio:
#   - La Superficie de Volatilidad muestra cómo cambia la volatilidad implícita según el precio de ejercicio y el tiempo
#     a vencimiento, revelando expectativas del mercado y niveles de riesgo para diferentes escenarios temporales.
