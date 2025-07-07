# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Definir Instrumento
ticker = "SPY" # ETF que replica el Índice S&P 500

# Definir función para cargar datos de opciones disponibles
def cargar_opciones(ticker: str):
    
    """
    Función que obtiene todas las opciones disponibles en el mercado.
    """
    
    # Extraer Datos
    asset = yf.Ticker(ticker=ticker)
    fechas_disponibles = asset.options
    # Iterar en cada fecha de vencimiento
    total_opciones_mercado = pd.DataFrame()
    for fecha in fechas_disponibles:
        # Descargar los datos para cada vencimiento
        opciones_vencimiento = asset.option_chain(date=fecha)
        calls = opciones_vencimiento.calls
        puts = opciones_vencimiento.puts
        # Agregar Datos Informativos
        calls["Type"] = "call"
        puts["Type"] = "put"
        # Unir y Ordenar
        opciones_concatenar = pd.concat([calls, puts], axis=0)
        opciones_concatenar = opciones_concatenar.sort_values(by="strike")
        # Agregar Fecha de Vencimiento
        opciones_concatenar["Expiration"] = fecha
        # Unir Todo en un DataFrame
        total_opciones_mercado = pd.concat([total_opciones_mercado, opciones_concatenar], axis=0)
        
    return asset, fechas_disponibles, total_opciones_mercado

# Obtener Total de Opciones
asset, fechas_disponibles, total_opciones_mercado = cargar_opciones(ticker=ticker)
print(total_opciones_mercado)

# =====================================
#  Skew (Sesgo) de Volatilidad Teórica
# =====================================

# El Skew de Volatilidad refleja cómo varía la volatilidad implícita entre opciones con diferentes
# precios de ejercicio. Se utiliza para identificar desequilibrios en la oferta y la demanda de opciones,
# revelando expectativas del mercado sobre posibles movimientos bruscos del activo subyacente.

# Existen diferentes Tipos de Sesgos:
    
# Definir Strikes Simulados
strikes = np.linspace(80, 120, 100)
atm_strike = 100

# Volatility Smile: La Volatilidad Implícita es mayor en opciones deep in-the-money y deep-out-the-money,
# y menor en los at-the-money. No es muy usual encontrarse con este sesgo.
smile = 0.2 + 0.001 * (strikes - atm_strike) ** 2

# Reverse Skew: La Volatilidad Implícita decrece al aumentar el strike. Usual en acciones, índices, ETFs
# de acciones, etc.
reverse_skew = 0.3 - 0.0015 * (strikes - atm_strike) + 0.00005 * (strikes - atm_strike) ** 2

# Forward Skew: La Volatilidad Implícita aumenta con el strike. Usual en Materias Primas con riesgo de escasez
# o shocks.
forward_skew = 0.2 + 0.0015 * (strikes - atm_strike) + 0.00005 * (strikes - atm_strike) ** 2 

# Volatility Frown: La Volatilidad Implícita es mayor en los at-the-money, y menor en los extremos (ITM y OTM).
# Poco común, pero puede aparecer cuando se espera estabilidad con baja probabilidad de movimientos extremos.
frown = 0.25 - 0.001 * (strikes - atm_strike) ** 2

# Crear subplots para mostrar sesgos
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(22, 12), dpi=300)
fig.suptitle("Sesgos de Volatilidad Implícita", fontsize=16)

# Sesgo 1: Volatility Smile
axs[0, 0].plot(strikes, smile, label="Smile", color="blue")
axs[0, 0].set_title("Volatility Smile (Sonrisa)")
axs[0, 0].set_xlabel("Precio de Ejercicio (Strike)")
axs[0, 0].set_ylabel("Volatilidad Implícita")
axs[0, 0].grid(True)

# Sesgo 2: Reverse Skew
axs[0, 1].plot(strikes, reverse_skew, label="Reverse Skew", color="red")
axs[0, 1].set_title("Reverse Skew (Sesgo Inverso)")
axs[0, 1].set_xlabel("Precio de Ejercicio (Strike)")
axs[0, 1].set_ylabel("Volatilidad Implícita")
axs[0, 1].grid(True)

# Sesgo 3: Forward Skew
axs[1, 0].plot(strikes, forward_skew, label="Forward Skew", color="green")
axs[1, 0].set_title("Forward Skew (Sesgo Positivo)")
axs[1, 0].set_xlabel("Precio de Ejercicio (Strike)")
axs[1, 0].set_ylabel("Volatilidad Implícita")
axs[1, 0].grid(True)

# Sesgo 4: Volatility Frown
axs[1, 1].plot(strikes, frown, label="Frown", color="purple")
axs[1, 1].set_title("Volatility Frown")
axs[1, 1].set_xlabel("Precio de Ejercicio (Strike)")
axs[1, 1].set_ylabel("Volatilidad Implícita")
axs[1, 1].grid(True)

plt.tight_layout()
plt.show()

# ==========================
#  Skew de Volatilidad Real
# ==========================

# Seleccionar 3 Diferentes Fechas
seleccion_fechas = [fechas_disponibles[5], fechas_disponibles[len(fechas_disponibles) // 2 + 6],
                    fechas_disponibles[-1]]
print(seleccion_fechas)

# Primera Fecha de Vencimiento
opciones_1 = total_opciones_mercado[total_opciones_mercado["Expiration"] == seleccion_fechas[0]]
calls_1 = opciones_1[opciones_1["Type"] == "call"]
puts_1 = opciones_1[opciones_1["Type"] == "put"]

# Segunda Fecha de Vencimiento
opciones_2 = total_opciones_mercado[total_opciones_mercado["Expiration"] == seleccion_fechas[1]]
calls_2 = opciones_2[opciones_2["Type"] == "call"]
puts_2 = opciones_2[opciones_2["Type"] == "put"]

# Tercera Fecha de Vencimiento
opciones_3 = total_opciones_mercado[total_opciones_mercado["Expiration"] == seleccion_fechas[2]]
calls_3 = opciones_3[opciones_3["Type"] == "call"]
puts_3 = opciones_3[opciones_3["Type"] == "put"]

# Unir Datos para comparar sesgos de volatilidad en distintos periodos
datos_combinados = [
    
    [calls_1, seleccion_fechas[0]],
    [calls_2, seleccion_fechas[1]],
    [calls_3, seleccion_fechas[2]],
    [puts_1, seleccion_fechas[0]],
    [puts_2, seleccion_fechas[1]],
    [puts_3, seleccion_fechas[2]]
    
    ]
precio_actual_activo = round(asset.info["regularMarketPrice"], 4)

# Generar Plot
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(22, 6))

# Graficar las volatilidades implícitas para cada vencimiento
colores = ["red", "blue", "green", "orange", "black", "purple"]
for n, ax in enumerate(axes.flatten()):
    ax.plot(datos_combinados[n][0]["strike"], datos_combinados[n][0]["impliedVolatility"], color=colores[n],
            label=f"Vencimiento: {datos_combinados[n][1]} " + ("Calls" if n<3 else "Puts"))
    ax.set_title(f"Volatilidad Implícita - {datos_combinados[n][1]} " + ("Calls" if n<3 else "Puts"))
    ax.set_xlabel("Strike Price")
    ax.set_ylabel("Volatilidad Implícita")
    ax.grid(True)
    ax.legend()

plt.suptitle(f"Skew de Volatilidad para {ticker} con Precio: {precio_actual_activo}")
plt.tight_layout()
plt.show()

# Recordatorio:
#   - El Sesgo de Volatilidad, nos ayuda a entender cómo varía la percepción del riesgo en el mercado respecto
#     a distintos precios de ejercicio. Al analizar la diferencia en volatilidad implícita entre opciones ITM,
#     ATM y OTM, podemos inferir expectativas de movimientos extremos y desequilibrio entre oferta y demanda.
