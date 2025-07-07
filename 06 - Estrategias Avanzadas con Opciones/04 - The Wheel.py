# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import datetime as dt
import finvizfinance.screener as screener 

# La estrategia sigue este ciclo:
    
# 1. Vender un put (cash-secured put)
#   - Esperas que la acción no caiga por debajo del strike.
#   - Si no se ejecuta -> cobras la prima
#   - Si se ejecuta -> compras la acción al strike (precio que ya querías de todos modos)

# Tarea Número 1: Encontrar Activos que tengan una posible tendencia alcista en el corto plazo (RSI_14 < 30)

# Utilizar Escáner para encontrar activos sobrevendidos:
screener_rsi = screener.overview.Overview()
filtro = "RSI (14)"
valores_filtracion = screener.get_filter_options(screen_filter=filtro)
print(valores_filtracion)
filtro_rsi = {
    
    filtro: "Oversold (30)"
    
    }
# Establecer Criterio
screener_rsi.set_filter(filters_dict=filtro_rsi)
screener_response = screener_rsi.screener_view()

# Ordenar en base al volumen (Seleccionar el primero que tenga múltiples fechas de vencimiento)
screener_response = screener_response.sort_values(by="Volume", ascending=False)
ticker_seleccionado = ""
try:
    for ticker in screener_response["Ticker"]: # Iteramos primero en los de mayor volumen
        # Generar Instancia
        asset = yf.Ticker(ticker=ticker)
        exp_dates = asset.options
        if len(exp_dates) > 8:
            ticker_seleccionado = ticker
            break
except Exception as error:
    print(f"Error con {ticker} ->", error)
    
# Seleccionar el primer vencimiento con más de 30 días (Es común usar puts de 30-45 días en The Wheel)
if ticker_seleccionado != "":
    asset = yf.Ticker(ticker=ticker_seleccionado)
    today = dt.date.today()
    exp_dates = asset.options
    # Seleccionar el primer vencimiento con más de 30 días 
    exp_sel = sorted([d for d in exp_dates if (pd.to_datetime(d).date() - today).days > 30])[0]
    dias_restantes = (pd.to_datetime(exp_sel).date() - today).days
    print(f"La fecha a utilizar tiene un total de {dias_restantes} días restantes hasta su vencimiento")
    options = asset.option_chain(date=exp_sel)
    puts = options.puts
    underlying_info = options.underlying
else:
    raise ValueError("No se ha encontrado ningún instrumento que cumpla con los requisitos")
    
# Obtener la prima de un contrato Put OTM
atm = underlying_info["regularMarketPrice"]
put = puts[puts["strike"] < atm].iloc[-1]
print(f"Precio Actual del Activo: {atm} | Prima a recibir: {put['bid'] * 100}")
    
# 2. Poseer la Acción
#   - Si te asignan las acciones, las mantienes.
#   - Ahora pasas a la siguiente fase del ciclo.

# Monto necesario para comprar las acciones
monto_total = put["strike"] * 100
print("Si fuesemos asignados al vencimiento necesitaríamos un monto aproximado de = {:.3f} USD".format(monto_total))

# 3. Vender un call (Covered Call)
#   - Sobre las acciones que posees.
#   - Si se ejecuta -> vendes las acciones al strike con ganancia.
#   - Si no se ejecuta -> cobrar la prima y repites

# Descargar Cadena de Opciones de los contratos que estaríamos usando para esta posición (+60 días restantes)
exp_sel = sorted([d for d in exp_dates if (pd.to_datetime(d).date() - today).days > 60])[0]
options = asset.option_chain(date=exp_sel)
calls = options.calls
indice = abs(calls["strike"] - atm * 1.05).argmin()
contrato = calls.iloc[indice]
print("Prima total a recibir: {}".format(contrato["bid"] * 100))

# ¿Cúal es el peor escenario en esta estrategia?
# El peor escenario en The Wheel ocurre cuando el precio de la acción cae fuertemente tras vender un put, eres asignado a un precio alto,
# y luego el activo sigue bajando, obligándote a mantener acciones en pérdida y dificultando vender calls rentables.

# Recordatorio:
#   - The Wheel es una estrategia donde vendes puts para cobrar primas, compras acciones si eres asignado, y luego vendes calls
#     cubiertas repetidamente para generar ingresos pasivos consistentes, aprovechando movimientos laterales o alcistas del mercado
#     mientras reduces el costo base de tus acciones con cada ciclo.
