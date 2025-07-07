# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf # pip install yfinance -> API de Yahoo Finance
from datetime import datetime
import pandas as pd
import json

# Elegir un Ticker para extraer opciones disponibles
ticker = "MSFT"

# Definir una instancia para extraer los datos
accion = yf.Ticker(ticker=ticker)

# Obtener todas las fechas disponibles de vencimiento
fechas_expiracion = accion.options

fecha_hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
print("Fechas de Expiración Disponibles para: {}\n".format(ticker))
for n, fecha in enumerate(fechas_expiracion):
    # Calcular el Tiempo Restante para cada fecha
    tiempo_restante = (pd.to_datetime(fecha) - fecha_hoy).days
    print(f" - Fecha No. {n + 1}:", fecha, "- Días Restantes ->", tiempo_restante)
    
print(f"\nHay un total de {n + 1} diferentes fechas de vencimiento")

# Seleccionar una Fecha de Vencimiento para obtener todos los precios de ejercicio disponibles
fecha_objetivo = fechas_expiracion[2]
print(f"\nDescargando opciones para la fecha: {fecha_objetivo}")

# Extraer Cadena de Opciones (Calls y Puts) para la fecha seleccionada
cadena_opciones = accion.option_chain(date=fecha_objetivo)
print(type(cadena_opciones))

# Extraer Información
calls, puts, underlying_info = cadena_opciones.calls, cadena_opciones.puts, cadena_opciones.underlying

print(f"\nOpciones Disponibles de Tipo Call para {ticker} en la fecha {fecha_objetivo}:")
print(calls)

print(f"\nOpciones Disponibles de Tipo Put para {ticker} en la fecha {fecha_objetivo}:")
print(puts)

print(f"Información del Activo Subyacente ({ticker}):\n")
print(json.dumps(underlying_info, indent=4))

# Revisar Cantidad de Contratos Generados
if calls.shape[0] > puts.shape[0]:
    print("Hay una mayor cantidad de contratos generados para los calls que para los puts...")
elif calls.shape[0] < puts.shape[0]:
    print("Hay una mayor cantidad de contratos generados para los puts que para los calls...")
else:
    print("La Cantidad de Contratos generados es la misma para los calls y puts.")
    
# Extraer Todos los Contratos Disponibles en todas las fechas de vencimiento
contratos_disponibles = pd.DataFrame()
for expiration_date in fechas_expiracion:
    # Extraer Cadena de Opciones para cada fecha
    calls, puts, _ = accion.option_chain(date=expiration_date)
    # Agregar Tipo de Opción
    calls["Option Type"] = "Call"
    puts["Option Type"] = "Put"
    # Agregar Días Restantes
    dias_faltantes = (pd.to_datetime(expiration_date) - fecha_hoy).days
    calls["Days to Expiration"] = dias_faltantes
    puts["Days to Expiration"] = dias_faltantes
    # Agregar Fecha de Vencimiento
    calls["Expiration Date"] = expiration_date
    puts["Expiration Date"] = expiration_date
    # Combinar Todo en el DataFrame
    contratos_disponibles = pd.concat([contratos_disponibles, calls, puts], ignore_index=True)

# Resumen Estadístico
total_calls = contratos_disponibles[contratos_disponibles["Option Type"] == "Call"].shape[0]
total_puts = contratos_disponibles[contratos_disponibles["Option Type"] == "Put"].shape[0]

print(f"\nResumen Estadístico para {ticker}:")
print(f" - Total de Contratos Call: {total_calls}")
print(f" - Total de Contratos Put: {total_puts}")
print(f" - Total de Contratos: {contratos_disponibles.shape[0]}")

# Entender el nombre del contrato
contrato_simbolo = contratos_disponibles["contractSymbol"].iloc[-1]
print(f"\nSímbolo del contrato: {contrato_simbolo}")

# Descomponer símbolo
ticker = contrato_simbolo[:-15]
fecha = pd.to_datetime(contrato_simbolo[-15:-9], format="%y%m%d") # YYMMDD : 271217
tipo = contrato_simbolo[-9] # "C" o "P"
strike_raw = int(contrato_simbolo[-8:]) / 1_000

print(f"Ticker: {ticker} | Fecha: {fecha} | Tipo: {'Call' if tipo == 'C' else 'Put'} | Strike: {strike_raw}")

# Recordatorio:
#   - La Cadena de Opciones es un conjunto de contratos de opciones (calls y puts) disponibles para un activo en
#     una fecha específica, con distintos precios de ejercicio y fechas de vencimiento.
#   - Un Instrumento Financiero (por ejemplo, Apple, Microsoft, etc.) puede tener miles de contratos de opciones,
#     los cuales varían según la fecha de vencimiento, tipo (Call o Put) y precio de ejercicio.
