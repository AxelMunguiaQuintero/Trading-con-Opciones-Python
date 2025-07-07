# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import numpy as np
import pandas as pd

# Paso 1: Definir Portafolio
portafolio = pd.DataFrame([
    
    {"ticker": "AAPL", "tipo": "opcion_call", "contratos/titulos": 5, "delta": 0.60},
    {"ticker": "MSFT", "tipo": "opcion_put", "contratos/titulos": -3, "delta": -0.45},
    {"ticker": "TSLA", "tipo": "accion", "contratos/titulos": 200, "delta": 1.0}
    
    ])

# Paso 2: Descargar Precios Históricos
tickers = portafolio["ticker"].unique().tolist()
tickers.append("SPY")

data = yf.download(tickers, period="1y", interval="1d")["Close"]

# Paso 3: Calcular rendimientos diarios
returns = data.pct_change().dropna()
rend_mercado = returns["SPY"]

# Paso 4: Calcular Beta de cada activo -> Cov(rend. activo, rend. mercado) / Var(rend. mercado)
betas = {}
for ticker in portafolio["ticker"]:
    rend_activo = returns[ticker]
    # Calcular Covarianza y Varianza
    calculo = np.cov(rend_activo, rend_mercado)
    # [[var(ticker), cov(ticker, benchmark)], [cov(ticker, benchmark), var(benchmark)]]
    cov = calculo[0, 1]
    var = calculo[1, 1]
    # Determinar Beta
    beta = cov / var
    betas[ticker] = beta
    
# Añadir betas al portafolio
portafolio["beta"] = portafolio["ticker"].map(betas)

# Paso 5: Calcular delta total del portafolio y beta-weighted delta (Delta del Portafolio ajustada al mercado)
portafolio["delta_total"] = portafolio["delta"] * portafolio["contratos/titulos"] * \
                            portafolio["tipo"].apply(lambda x: 100 if "opcion" in x else 1)
                            
portafolio["beta_weighted_delta"] = portafolio["delta_total"] * portafolio["beta"]
portafolio.index = ["Activo 1", "Activo 2", "Activo 3"]

# Realizar cálculo de la Delta del Portafolio
delta_portafolio = portafolio["delta_total"].sum()
beta_delta_portafolio = portafolio["beta_weighted_delta"].sum()

# Resultados
print("Portafolio:\n")
print(portafolio.T)

print(f"\nDelta Total del Portafolio: {delta_portafolio:.2f}")
print(f"Beta-weighted Delta: {beta_delta_portafolio:.2f}")

titulos_spy_para_neutralizar = round(beta_delta_portafolio)
print(f"\nPara neutralizar el riesgo de mercado, podrías vender {titulos_spy_para_neutralizar} títulos de SPY")
print(
      "Un portafolio delta-neutral debe tener una delta total cercana a cero, idealmente menor al 1-2% del valor "
      "total (valor absoluto), para minimizar la sensibilidad a movimientos del subyacente y mantener estabilidad "
      "en la exposición al mercado."
      
      )

# Recordatorio:
#   - La Delta total del portafolio mide la sensibilidad del portafolio a cambios en el precio del subyacente,
#     indicando cuánto variará su valor ante movimientos pequeños. Nos ayuda a entener la exposición direccional
#     y a gestionar nuestro riesgo cuando buscamos portafolios neutrales al riesgo.
#   - La Beta-Weighted Delta ajusta la delta de cada posición según su beta relativa al mercado, reflejando la exposición
#     total del portafolio frente a movimientos generales del índice de referencia. Es útil para evaluar y neutralizar
#     riesgos sistemáticos.
