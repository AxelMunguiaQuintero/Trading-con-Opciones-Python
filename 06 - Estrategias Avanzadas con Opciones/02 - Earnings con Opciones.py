# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
from finvizfinance.earnings import Earnings # pip install finvizfinance 
import pandas as pd
import numpy as np
from datetime import datetime

# Realizar Extracción de Datos
earnings_peticion = Earnings(period="This Month") # Posibles Valores: "This Week", "Next Week", "Previos Week", "This Month"
print(earnings_peticion.earning_days)

# Extraer Datos en un DataFrame
earnings_df = earnings_peticion.df # /a -> "After Market Close", /b -> "Before Market Open"

# Ajustar Fecha y Tiempo de Anuncio
hoy = datetime.now()
earnings_df = earnings_df[earnings_df["Earnings"].apply(lambda x: "/a" in x or "/b" in x)].copy()
earnings_df[["Earnings", "Earnings Call Time"]] = earnings_df["Earnings"].str.split("/").tolist()
earnings_df["Earnings"] = pd.to_datetime(earnings_df["Earnings"], format="%b %d").apply(lambda x: x.replace(year=hoy.year))
earnings_df["Earnings Call Time"] = earnings_df["Earnings Call Time"].replace({
    
    "a": "After Market Close",
    "b": "Before Market Open"
    
    })

# Filtrar en Base a Criterios:
# Criterio 1: Elegir empresas que reporten "After Market Close" (puedes abrir la posición antes del evento)
# Criterio 2: Empresas con ROIC alto (>=10%) suelen estar bien gestionadas
# Criterio 3: Empresas con dividendos altos tienden a ser más estables (>=2% para menor movimiento) -> Opcional
# Criterio 4: Liquidez alta para que existan opciones activas con spreads razonables (Volumen > 300,000)
# Criterio 5: Acciones con precio superior a $20 (porque son más líquidas en opciones y tienen spreads razonables)
# Criterio 6: Empresas mid-cap o large-cap generan interés (Market Cap >1e9)
filtro = (
    
    (earnings_df["Earnings Call Time"] == "After Market Close") &
    (earnings_df["ROIC"].str.rstrip("%").str.replace("-", "0").astype(float) >= 10) &
    # (earnings_df["Dividen"] >= 0.02) &
    (earnings_df["Volume"] > 300_000) & 
    (earnings_df["Price"] > 20) &
    (earnings_df["Market Cap"] > 1e9)   
    
    )

candidatos = earnings_df[filtro].set_index("Ticker")
# Filtrar a aquellas empresas que no hay realizado su reporte de ganancias
# candidatos = candidatos[candidatos["Earnings"] > hoy]
print(candidatos)

# Calcular el Valor del "Implied Move": Este es el rango de movimiento que el mercado espera para un activo hasta cierta fecha,
# calculado sumando las primas de la call y put ATM.
im = []
for ticker in candidatos.index:
    # Crear Instancia del Activo
    activo = yf.Ticker(ticker=ticker)
    # Descargar Fechas y Seleccionar la siguiente después del anuncio (Aseguramos que el contrato será afectado por la IV)
    fechas_disponibles = np.array([pd.to_datetime(fecha) for fecha in activo.options])
    fecha_earnings = pd.to_datetime(candidatos.loc[ticker, "Earnings"])
    fechas_superiores = fechas_disponibles[fechas_disponibles > fecha_earnings]
    fecha_seleccionada = fechas_superiores[0].strftime("%Y-%m-%d")
    # Descargar Cadena de Opciones
    try:
        # Extraer Datos
        calls, puts, underlying_info = activo.option_chain(date=fecha_seleccionada)
        precio_actual = underlying_info["regularMarketPrice"]
        # Seleccionar Contratos ATM
        indice = abs(calls["strike"] - precio_actual).argmin()
        strike = calls.iloc[indice]["strike"]
        contrato_call = calls[calls["strike"] == strike]
        contrato_put = puts[puts["strike"] == strike]
        # Obtener Implied Move
        movimiento_unidades = contrato_call["bid"].iloc[0] + contrato_put["bid"].iloc[0] # Representado en Dólares
        movimiento_porcentaje = movimiento_unidades / precio_actual * 100
        im.append([movimiento_unidades, movimiento_porcentaje])
    except:
        im.append([np.nan, np.nan])
        
# Agregar info a la tabla
candidatos["IM Unidades"] = np.array(im)[:, 0]
candidatos["IM Porcentaje"] = np.array(im)[:, 1]

# Eliminar Candidatos sin IM
candidatos = candidatos[candidatos["IM Unidades"].notna()]
print(candidatos)

# Obtener fechas anteriores de sus Earnings
earnings_anteriores = []
for ticker in candidatos.index:
    try:
        activo = yf.Ticker(ticker=ticker)
        # Obtener los Earnings anteriores y quedarnos con los 3 más recientes
        eanings_dates = activo.earnings_dates.iloc[:3]
        eanings_dates.index = eanings_dates.index.strftime("%Y-%m-%d")
        earnings_anteriores.append(eanings_dates)
    except:
        earnings_anteriores.append(np.nan)

# Desplegar los datos para una empresa
print(earnings_anteriores[0])

# Descargar Datos
datos = []
for n, ticker in enumerate(candidatos.index):
    # Descargar Datos
    df = yf.download(tickers=ticker, start=earnings_anteriores[n].index[-1], end=None,
                     interval="1d", multi_level_index=False)
    # Calcular Rendimientos
    rendimientos = df["Close"].pct_change()
    # Extraer Fechas donde sucedió el cambio (Ordenar Datos)
    cambios = ["{:.4f}%".format(rendimientos.loc[fecha:].iloc[1] * 100)
              for fecha in earnings_anteriores[n].index[::-1]]
    movimientos_pasados = pd.DataFrame(index=earnings_anteriores[n].index[::-1], data=cambios, columns=["Cambio"])
    datos.append(movimientos_pasados)

# Mostrar por Consola
for n, ticker in enumerate(candidatos.index):
    print("\nImplied Move:\n")
    print(candidatos.loc[ticker, ["IM Unidades", "IM Porcentaje"]].to_frame().T)
    print("\nMovimientos Anteriores de Earnings:\n")
    print(datos[n])

# Recordatorio:
#   - El Short Straddle y el Short Strangle son estrategias neutrales que buscan beneficiarse de la caída
#     en la volatilidad implícita (IV Crush) tras eventos como earnings. Se estructuran vendiendo opciones ATM,
#     esperando que el movimiento realizado esté dentro del rango implícito descontado.
#   - El Crush de volatilidad es la rápida caída de la volatilidad implícita tras un evento esperado, como earnings.
#     Reduce el valor estrínseco de las opciones, afectando negativamente posiciones compradas.
#   - En esta estrategia no se recomienda mantener mucho tiempo la posición (short straddle), pues la idea es
#     beneficiarse del crush de volatilidad, y evitar cualquier movimiento direccional prolongado del activo.
