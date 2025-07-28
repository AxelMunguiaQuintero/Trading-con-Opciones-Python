# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import finvizfinance.screener as screener
from yahooquery import Screener # pip install yahooquery
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from warnings import filterwarnings
filterwarnings("ignore")

# Capital total disponible para inversión
capital_total_usd = 10_000

# Porcentajes de asignación de capital
porcentaje_acciones = 0.60 # 60% del capital se destina a compra de acciones
porcentaje_opciones = 0.40 # 40% del capital se asigna a estrategias con opciones

# Asignación del capital destinado a opciones por tipo de riesgo
proporcion_riesgo_definido = 0.25  # Estrategias con riesgo definido (ej. spreads)
proporcion_riesgo_indefinido = 0.75 # Estrategias con riesgo indefinido (ej. venta naked)

# Cálculo del monto asignado a cada tipo de estrategia
capital_riesgo_definido = proporcion_riesgo_definido * (capital_total_usd * porcentaje_opciones)
capital_riesgo_indefinido = proporcion_riesgo_indefinido * (capital_total_usd * porcentaje_opciones)
capital_acciones = capital_total_usd * porcentaje_acciones

# Mostrar Montos
print(f"Capital destinado a Equity {capital_acciones:,}")
print(f"Capital Opciones -> Riesgo Definido: {capital_riesgo_definido:,} | Riesgo Indefinido: {capital_riesgo_indefinido:,}")

# Definir función para encontrar empresas con recomendaciones fuertes de compra
def recomendacion_compra(escaner: str = "analyst_strong_buy_stocks", capital_inversion: float = capital_acciones):
    
    """
    Genera recomendaciones de compra de acciones con base en un escáner de analistas con un crecimiento mínimo del 20%
    en un periodo de un año.
    """
    
    # Definir escáner
    escaner_instancia = Screener()
    respuesta = escaner_instancia.get_screeners(screen_ids=escaner, count=30)
    # Extraer Empresas
    empresas = [[empresa["ticker"], empresa["regularMarketPrice"], empresa["priceTargetCurrent"]]
                for empresa in respuesta[escaner]["records"]]
    empresas = pd.DataFrame(empresas, columns=["Ticker", "Precio Actual", "Precio Estimado"])
    
    # Ordenar empresas en base al crecimiento esperado
    empresas["Crecimiento %"] = empresas["Precio Estimado"] / empresas["Precio Actual"] - 1
    empresas = empresas.sort_values(by="Crecimiento %", ascending=False)
    indice = [f"Activo {i}" for i in range(len(empresas))]
    empresas.index = indice
    
    # Invertir más en las empresas que más crecerán (Ponderar los valores)
    empresas["Ponderacion"] = empresas["Crecimiento %"] / empresas["Crecimiento %"].sum()
    
    # Calcular cuantas acciones compraremos
    empresas["Capital Asignado"] = empresas["Ponderacion"] * capital_inversion
    empresas["No. Titulos"] = np.floor(empresas["Capital Asignado"] / empresas["Precio Actual"])
    
    return empresas

# Obtener Empresas
empresas = recomendacion_compra()
print(empresas.T)
    
# Definir función para encontrar activos para nuestras estrategias con Opciones
def activos_opciones():
    
    """
    Identifica activos adecuados para estrategias con Opciones, clasificadas por tipo de riesgo (definido o indefinido),
    utilizando señales técnicas desde el escáner de Finviz.
    """
    
    # Estrategias Riesgo Definido:
        
    # Estrategia Bull Call Spread (Débito) | Escáner: Channel Up -> Este escáner identifica acciones que están operando
    # dentro de un canal ascedente, sugiriendo una tendencia alcista con máximos y mínimos crecientes bien definidos.
    escaner_channel_up = screener.overview.Overview()
    escaner_channel_up.set_filter(signal="Channel Up")
    respuesta_channel_up = escaner_channel_up.screener_view(order="Analyst Recommendation")
    
    # Ordenar en base a la Capitalización de Mercado y Volume (Mayor Interés de Inversionistas)
    respuesta_channel_up = respuesta_channel_up.sort_values(by="Market Cap", ascending=False)
    
    # Filtrar Activos (Volumen > 1_000_000)
    respuesta_channel_up = respuesta_channel_up[respuesta_channel_up["Volume"] >= 1_000_000]
    
    # Dormir 10 Segundos (Evitar Bloqueos)
    time.sleep(10)
    
    # Estrategia Bear Put Spread (Débito) | Escáner: Channel Down -> Detecta acciones que se mueven dentro de un canal
    # descendente, caracterizado por una tendencia bajista con máximos y mínimos decrecientes de forma constante.
    escaner_channel_down = screener.overview.Overview()
    escaner_channel_down.set_filter(signal="Channel Down")
    respuesta_channel_down = escaner_channel_down.screener_view(order="Market Cap.", ascend=False)
    
    # Filtrar Activos (Volumen > 1_000_000)
    respuesta_channel_down = respuesta_channel_down[respuesta_channel_down["Volume"] >= 1_000_000]
    
    # Dormir 10 Segundos (Evitar Bloqueos)
    time.sleep(10)
    
    # Estrategias Riesgo Indefinido:
        
    # Estrategia Short Call (Crédito) | TL Resistance -> Identifica acciones que están tocando o acercándose a una línea
    # de tendencia superior, lo que podría indicar una posible resistencia técnica y reversión bajista.
    tl_resistance = screener.overview.Overview()
    tl_resistance.set_filter(signal="TL Resistance")
    respuesta_tl_resistance = tl_resistance.screener_view(order="Market Cap.", ascend=False)
    
    # Filtrar Activos (Volumen > 1_000_000)
    respuesta_tl_resistance = respuesta_tl_resistance[respuesta_tl_resistance["Volume"] >= 1_000_000]
    
    # Dormir 10 Segundos (Evitar Bloqueos)
    time.sleep(10)
    
    # Estrategia Short Put (Crédito) | TL Support -> Detecta acciones que están tocando o acercándose a una línea de tendencia
    # inferior, sugiriendo una posible zona de soporte donde el precio podría rebotar.
    tl_support = screener.overview.Overview()
    tl_support.set_filter(signal="TL Support")
    respuesta_tl_support = tl_support.screener_view(order="Market Cap.", ascend=False)
    
    # Filtrar Activos (Volumen > 1_000_000)
    respuesta_tl_support = respuesta_tl_support[respuesta_tl_support["Volume"] >= 1_000_000]
    
    return respuesta_channel_up, respuesta_channel_down, respuesta_tl_resistance, respuesta_tl_support

# Obtener Activos
respuesta_channel_up, respuesta_channel_down, respuesta_tl_resistance, respuesta_tl_support = activos_opciones()
print("Total de Activos encontrados (Channel Up):", respuesta_channel_up.shape[0])
print("Total de Activos encontrados (Channel Down):", respuesta_channel_down.shape[0])
print("Total de Activos encontrados (TL Resistance):", respuesta_tl_resistance.shape[0])
print("Total de Activos encontrados (TL Support):", respuesta_tl_support.shape[0])
    
# Definir función para obtener los contratos
def obtener_contratos(respuesta_channel_up: pd.DataFrame = respuesta_channel_up,
                      respuesta_channel_down: pd.DataFrame = respuesta_channel_down,
                      respuesta_tl_resistance: pd.DataFrame = respuesta_tl_resistance,
                      respuesta_tl_support: pd.DataFrame = respuesta_tl_support):
    
    """
    Obtiene contratos de opciones adecuados para cada estrategia de trading en función del activo.
    """
    
    # Filtrar en Estrategia Bull Call Spread (Channel Up)
    activos_interes = []
    contratos = []
    for ticker in respuesta_channel_up["Ticker"]:
        activo = yf.Ticker(ticker=ticker)
        # Obtener Vencimientos
        fechas_disponibles = activo.options
        if len(fechas_disponibles) >= 6:
            try:
                # Seleccionar contrato con más de 30 días restantes al vencimiento
                hoy = datetime.now()
                hoy_30 = hoy + timedelta(days=30)
                fecha_seleccionada = [fecha for fecha in fechas_disponibles if pd.to_datetime(fecha) >= hoy_30][0]
                # Obtener Cadena de Opciones
                opciones = activo.option_chain(date=fecha_seleccionada)
                calls = opciones.calls
                # Obtener Contratos (Bull Call Spread: Comprar Call K1 + Vender Call K2 con K1 < K2)
                info = activo.info
                precio_actual = info["regularMarketPrice"]
                K1 = precio_actual * 0.98 # Precio de Ejercicio Ideal +1 Call K1
                K2 = precio_actual * 1.02 # Precio de Ejercicio Ideal -1 Call K2
                contrato_K1 = calls[calls["strike"] <= K1].iloc[-1]
                contrato_K2 = calls[calls["strike"] >= K2].iloc[0] 
                
                # Agregar Información (Validar Si existen)
                if not (contrato_K1.empty or contrato_K2.empty):
                    contratos.append([contrato_K1, contrato_K2])
                    activos_interes.append(True)
                else:
                    activos_interes.append(False)
                
            except:
                activos_interes.append(False)
        else:
            activos_interes.append(False)
    
    # Eliminar Activos que no son de nuestro interés
    respuesta_channel_up = respuesta_channel_up.loc[activos_interes]
    
    # Agregar Información
    if not respuesta_channel_up.empty:
        respuesta_channel_up["contratos"] = contratos
        
    # Filtrar en Estrategia Bear Put Spread (Channel Down)
    activos_interes = []
    contratos = []
    for ticker in respuesta_channel_down["Ticker"]:
        activo = yf.Ticker(ticker=ticker)
        # Obtener Vencimientos
        fechas_disponibles = activo.options
        if len(fechas_disponibles) >= 6:
            try:
                # Seleccionar contrato con más de 30 días restantes al vencimiento
                hoy = datetime.now()
                hoy_30 = hoy + timedelta(days=30)
                fecha_seleccionada = [fecha for fecha in fechas_disponibles if pd.to_datetime(fecha) >= hoy_30][0]
                # Obtener Cadena de Opciones
                opciones = activo.option_chain(date=fecha_seleccionada)
                puts = opciones.puts
                # Obtener Contratos (Bear Put Spread: Vender Put K1 + Comprar Put K2 con K1 < K2)
                info = activo.info
                precio_actual = info["regularMarketPrice"]
                K1 = precio_actual * 0.98 # Precio de Ejercicio Ideal -1 Put K1
                K2 = precio_actual * 1.02 # Precio de Ejercicio Ideal +1 Put K2
                contrato_K1 = puts[puts["strike"] <= K1].iloc[-1]
                contrato_K2 = puts[puts["strike"] >= K2].iloc[0]
                
                # Agregar Información (Validar Si existen)
                if not (contrato_K1.empty or contrato_K2.empty):
                    contratos.append([contrato_K1, contrato_K2])
                    activos_interes.append(True)
                else:
                    activos_interes.append(False)
                
            except:
                activos_interes.append(False)
        else:
            activos_interes.append(False)
    
    # Eliminar Activos que no son de nuestro interés
    respuesta_channel_down = respuesta_channel_down.loc[activos_interes]
    
    # Agregar Información
    if not respuesta_channel_down.empty:
        respuesta_channel_down["contratos"] = contratos
        
    # Filtrar en Estrategia Short Call (TL Resistance)
    activos_interes = []
    contratos = []
    for ticker in respuesta_tl_resistance["Ticker"]:
        activo = yf.Ticker(ticker=ticker)
        # Obtener Vencimientos
        fechas_disponibles = activo.options
        if len(fechas_disponibles) >= 6:
            try:
                # Seleccionar contrato con más de 30 días restantes al vencimiento
                hoy = datetime.now()
                hoy_30 = hoy + timedelta(days=30)
                fecha_seleccionada = [fecha for fecha in fechas_disponibles if pd.to_datetime(fecha) >= hoy_30][0]
                # Obtener Cadena de Opciones
                opciones = activo.option_chain(date=fecha_seleccionada)
                calls = opciones.calls
                # Obtener Contrato ATM
                info = activo.info
                precio_actual = info["regularMarketPrice"]
                indice = abs(calls["strike"] - precio_actual).argmin()
                contrato = calls.iloc[indice]
                
                # Agregar Información (Validar Si existe)
                if not contrato.empty:
                    contratos.append([contrato])
                    activos_interes.append(True)
                else:
                    activos_interes.append(False)
                
            except:
                activos_interes.append(False)
        else:
            activos_interes.append(False)
    
    # Eliminar Activos que no son de nuestro interés
    respuesta_tl_resistance = respuesta_tl_resistance.loc[activos_interes]
    
    # Agregar Información
    if not respuesta_tl_resistance.empty:
        respuesta_tl_resistance["contratos"] = contratos
        
    # Filtrar en Estrategia Short Put (TL Support)
    activos_interes = []
    contratos = []
    for ticker in respuesta_tl_support["Ticker"]:
        activo = yf.Ticker(ticker=ticker)
        # Obtener Vencimientos
        fechas_disponibles = activo.options
        if len(fechas_disponibles) >= 6:
            try:
                # Seleccionar contrato con más de 30 días restantes al vencimiento
                hoy = datetime.now()
                hoy_30 = hoy + timedelta(days=30)
                fecha_seleccionada = [fecha for fecha in fechas_disponibles if pd.to_datetime(fecha) >= hoy_30][0]
                # Obtener Cadena de Opciones
                opciones = activo.option_chain(date=fecha_seleccionada)
                puts = opciones.puts
                # Obtener Contrato ATM
                info = activo.info
                precio_actual = info["regularMarketPrice"]
                indice = abs(puts["strike"] - precio_actual).argmin()
                contrato = puts.iloc[indice]
                
                # Agregar Información (Validar Si existe)
                if not contrato.empty:
                    contratos.append([contrato])
                    activos_interes.append(True)
                else:
                    activos_interes.append(False)
                
            except:
                activos_interes.append(False)
        else:
            activos_interes.append(False)
    
    # Eliminar Activos que no son de nuestro interés
    respuesta_tl_support = respuesta_tl_support.loc[activos_interes]
    
    # Agregar Información
    if not respuesta_tl_support.empty:
        respuesta_tl_support["contratos"] = contratos
        
    return respuesta_channel_up, respuesta_channel_down, respuesta_tl_resistance, respuesta_tl_support
        
respuesta_channel_up, respuesta_channel_down, respuesta_tl_resistance, respuesta_tl_support = obtener_contratos()

# Mostrar Totalidad de Activos Restantes
print("Total de Activos encontrados (Channel Up):", respuesta_channel_up.shape[0])
print("Total de Activos encontrados (Channel Down):", respuesta_channel_down.shape[0])
print("Total de Activos encontrados (TL Resistance):", respuesta_tl_resistance.shape[0])
print("Total de Activos encontrados (TL Support):", respuesta_tl_support.shape[0])
    
# Quedarme con las primeras 2 Posiciones de cada respuesta
respuesta_channel_up = respuesta_channel_up.iloc[:2]
respuesta_channel_down = respuesta_channel_down.iloc[:2]
respuesta_tl_resistance = respuesta_tl_resistance.iloc[:2]
respuesta_tl_support = respuesta_tl_support.iloc[:2]

# Describir Posiciones (Acciones)
print("\nPosiciones con Acciones:\n")
for indice, empresa in empresas.iterrows():
    print(f"Compraremos {empresa['No. Titulos']} títulos de {empresa['Ticker']} a {empresa['Precio Actual']}")
    
# Describir Posiciones Opciones (Riesgo Indefinido: Short Call)
print("\nPosiciones con Opciones (Riesgo Indefinido - Short Call):\n")
for indice, empresa in respuesta_tl_resistance.iterrows():
    print(
        
        f"Venderemos un Contrato Call de {empresa['Ticker']} con Strike {empresa['contratos'][0]['strike']}. "
        f" Recibiremos una prima de {empresa['contratos'][0]['bid'] * 100:.4f}. "
        f" Con Vencimiento {pd.to_datetime(empresa['contratos'][0]['contractSymbol'][-15:-9], format='%y%m%d')}"
        
        )
    
# Describir Posiciones Opciones (Riesgo Indefinido: Short Put)
print("\nPosiciones con Opciones (Riesgo Indefinido - Short Put):\n")
for indice, empresa in respuesta_tl_support.iterrows():
    print(
        
        f"Venderemos un Contrato Put de {empresa['Ticker']} con Strike {empresa['contratos'][0]['strike']}. "
        f" Recibiremos una prima de {empresa['contratos'][0]['bid'] * 100:.4f}. "
        f" Con Vencimiento {pd.to_datetime(empresa['contratos'][0]['contractSymbol'][-15:-9], format='%y%m%d')}"
        
        )
    
# Describir Posiciones Opciones (Riesgo Definido: Bull Call Spread)
print("\nPosiciones con Opciones (Riesgo Definido - Bull Call Spread):\n")
for indice, empresa in respuesta_channel_up.iterrows():
    print(
        
        f"Compraremos un Contrato Call de {empresa['Ticker']} con Strike {empresa['contratos'][0]['strike']}. "
        f"Adicionalmente, venderemos un Call de {empresa['Ticker']} con Strike {empresa['contratos'][1]['strike']}. "
        f"Con Vencimiento: {pd.to_datetime(empresa['contratos'][0]['contractSymbol'][-15:-9], format='%y%m%d')}. "
        f"Pagaremos un Débito de {(empresa['contratos'][0]['ask'] - empresa['contratos'][1]['bid']) * 100:.3f}"
        
        )
    
# Describir Posiciones Opciones (Riesgo Definido: Bear Put Spread)
print("\nPosiciones con Opciones (Riesgo Definido - Bear Put Spread):\n")
for indice, empresa in respuesta_channel_down.iterrows():
    print(
        
        f"Venderemos un Contrato Put de {empresa['Ticker']} con Strike {empresa['contratos'][0]['strike']}. "
        f"Adicionalmente, compraremos un Put de {empresa['Ticker']} con Strike {empresa['contratos'][1]['strike']}. "
        f"Con Vencimiento: {pd.to_datetime(empresa['contratos'][0]['contractSymbol'][-15:-9], format='%y%m%d')}. "
        f"Pagaremos un Débito de {(empresa['contratos'][1]['ask'] - empresa['contratos'][0]['bid']) * 100:.3f}"
        
        )
