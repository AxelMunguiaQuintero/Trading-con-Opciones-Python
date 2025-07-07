# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt

# Seleccionar ticker
ticker = "SPY"

# Extraer todas las opciones disponibles
activo = yf.Ticker(ticker=ticker)
precio_actual = round(activo.info["regularMarketPrice"], 4)
# Realizar Peticiones de Datos
total_peticiones = [activo.option_chain(date=fecha) for fecha in activo.options]
extraer_opciones = [pd.concat([extraccion.calls, extraccion.puts], axis=0) for extraccion in total_peticiones]
opciones_totales = pd.concat(extraer_opciones, axis=0)
# Agregar Información (Tipo de Opción y Fecha de Vencimiento)
opciones_totales["Type"] = opciones_totales["contractSymbol"].apply(lambda x: "call" if x[-9] == "C" else "put")
func_expiration = lambda x: pd.to_datetime(x[-15:-9], format="%y%m%d")
opciones_totales["Expiration"] = opciones_totales["contractSymbol"].apply(func_expiration)

# Guardar
if not os.path.isdir("../datos"):
    os.mkdir("../datos")
opciones_totales.to_csv("../datos/opciones.csv")

# =================
#  Term Structura
# =================

# El Term Structure es la relación entre la volatilidad implícita de las opciones y el tiempo hasta su vencimiento.
# Refleja cómo el mercado anticipa cambios en la volatilidad futura según distintos horizontes temporales,
# clave para estrategias y valuación.

# Elegir el strike ATM
indice_atm = abs(opciones_totales["strike"] - precio_actual).argmin()
strike_seleccionado = int(opciones_totales.iloc[indice_atm]["strike"])
print("Strike Seleccionado:", strike_seleccionado)

# Calls ATM
calls_atm = opciones_totales[(opciones_totales["strike"] == strike_seleccionado) & (opciones_totales["Type"] == "call")]

# Puts ATM
puts_atm = opciones_totales[(opciones_totales["strike"] == strike_seleccionado) & (opciones_totales["Type"] == "put")]

# Graficar
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(22, 6))

# Configurar gráfico de Calls ATM
axes[0].plot(pd.to_datetime(calls_atm["Expiration"]), calls_atm["impliedVolatility"], marker="o", 
             label=f"Calls ATM (Strike: {strike_seleccionado})", color="blue")
axes[0].set_title(f"Term Structure - Call ATM ({ticker})")
axes[0].set_xlabel("Fechas de Vencimiento")
axes[0].set_ylabel("Volatilidad Implícita")
axes[0].grid()
axes[0].legend()

# Configurar gráfico de puts ATM
axes[1].plot(pd.to_datetime(puts_atm["Expiration"]), puts_atm["impliedVolatility"], marker="o", 
             label=f"Puts ATM (Strike: {strike_seleccionado})", color="red")
axes[1].set_title(f"Term Structure - Put ATM ({ticker})")
axes[1].set_xlabel("Fechas de Vencimiento")
axes[1].set_ylabel("Volatilidad Implícita")
axes[1].grid()
axes[1].legend()

plt.suptitle(f"Estructura Temporal de Volatilidad Implícita (Precio {ticker}): {precio_actual:.3f}")
plt.tight_layout()
plt.show()

# Recordatorio:
#   - La Estructura Temporal (Term Structura) nos permite observar cómo varía la volatilidad implícita según el tiempo
#     restante hasta el vencimiento de las opciones.
