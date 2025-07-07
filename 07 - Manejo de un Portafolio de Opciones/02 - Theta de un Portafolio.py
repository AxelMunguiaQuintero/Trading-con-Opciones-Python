# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from alpha_vantage.options import Options
import pandas as pd
import numpy as np
import json

# Crear Cliente con Alpha Vantage
clave_api = "API_KEY"
cliente = Options(key=clave_api)

# Definir Tickers para diferentes posiciones
tickers = ["AAPL", "MSFT", "TSLA"]

# Obtener fechas de vencimiento
datos = {}
for ticker in tickers:
    activo = yf.Ticker(ticker=ticker)
    fechas_disponibles = activo.options
    # Elegir una fecha de random
    fecha_seleccionada = np.random.choice(fechas_disponibles, size=1)[0]
    # Obtener Precio Actual
    precio = activo.info["regularMarketPrice"]
    # Seleccionar un strike distinto (random)
    variacion = [0.80, 0.90, 1.0, 1.10, 1.20]
    strike = precio * np.random.choice(variacion, size=1)[0]
    # Almacenar Datos
    datos[ticker] = {"fecha": fecha_seleccionada, "precio": precio, "strike": strike}
    
print(json.dumps(datos, indent=4))

# Simulación del Portafolio
portafolio = {
    
    "AAPL": {"tipo": "call", "strike": datos["AAPL"]["strike"], "vencimiento": datos["AAPL"]["fecha"], "posicion": 3},
    "MSFT": {"tipo": "put", "strike": datos["MSFT"]["strike"], "vencimiento": datos["MSFT"]["fecha"], "posicion": -8},
    "TSLA": {"tipo": "call", "strike": datos["TSLA"]["strike"], "vencimiento": datos["TSLA"]["fecha"], "posicion": 2}
    
    }

# Extraer Cadena de Opciones para cada posición
contratos = {}
for ticker in tickers:
    opciones, _ = cliente.get_historical_options(symbol=ticker)
    # Filtrar en base al vencimiento y al tipo de opción
    contratos_seleccionados = opciones[(opciones["expiration"] == portafolio[ticker]["vencimiento"]) & \
                                       (opciones["type"] == portafolio[ticker]["tipo"])]
    # Encontrar el contrato más cercano al strike seleccionado
    indice_strike = abs(contratos_seleccionados["strike"].apply(float) - portafolio[ticker]["strike"]).argmin()
    contrato = contratos_seleccionados.iloc[indice_strike]
    contratos[ticker] = contrato
    
# Realizar el cálculo de la theta del portafolio
thetas_individuales = {}
for ticker in tickers:
    # Obtener Theta de cada contrato
    thetas_individuales[ticker] = {"Theta": float(contratos[ticker]["theta"]) * 100 * portafolio[ticker]["posicion"]}

# Convertir a DataFrame
thetas = pd.DataFrame(thetas_individuales)
print(thetas)

# Calcular la Theta total del portafolio
theta_total = thetas.sum(axis=1).values[0]
print(f"\n>>> Theta del Portafolio: {theta_total:.2f} USD/día")

# Definir el capital total de nuestro portafolio
capital_total = 100_000

# Definir un porcentaje destinado a estrategias de ingreso (premium selling)
porcentaje_objetivo = 0.25 # 25% para vender opciones con Theta Positiva
capital_asignado = capital_total * porcentaje_objetivo
horizonte_temporal_recomendado = "30-45 días"
theta_positiva_diaria_ingreso = 0.002 # Se recomiend tener un ingreso del 0.2% diario
liquidez_diaria = capital_asignado * theta_positiva_diaria_ingreso

# Desplegar Datos
print(f"Capital Total -> ${capital_total:,.2f}")
print(f"Capital Asignado (Premium Selling -> ${capital_asignado:,.2f}")
print(f"Horizonte Temporal Recomendado -> {horizonte_temporal_recomendado}")
print(f"Ingreso Estimado Diario por Theta -> ${liquidez_diaria:,.2f}")
print(f"Ingreso Estimado Anual (Theta x 365) -> ${liquidez_diaria * 365:,.2f}")

# Recordatorio:
#   - La theta del portafolio representa la sensibilidad total al paso del tiempo. Una theta positiva indica que
#     cada día genera una ganancia esperada. Esto es ideal para estrategias que buscan ingresos consistentes mediante
#     la venta de opciones.
#   - La liquidez diaria basada en theta permite proyectar ingresos diarios aproximados por el tiempo. Esta métrica
#     ayuda a dimensionar el capital necesario y ajustar posiciones para cumplir metas de flujo constante en estrategias
#     premium selling.
