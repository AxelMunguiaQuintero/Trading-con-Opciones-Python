# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import numpy as np

# Portafolio con Vegas
portafolio = pd.DataFrame([
    
    {"activo": "AAPL", "tipo": "opcion_call", "contratos/titulos": 10, "vega": 0.18},
    {"activo": "MSFT", "tipo": "opcion_put", "contratos/titulos": -5, "vega": 0.22},
    {"activo": "TSLA", "tipo": "opcion_call", "contratos/titulos": -3, "vega": 0.12},
    {"activo": "TSLA acciones", "tipo": "accion", "contratos/titulos": 100, "vega": 0.0}
    
    ], index=[f"Activo {i}" for i in range(1, 5)])

# Calcular Vega del Portafolio
portafolio["vega_portafolio"] = portafolio["vega"] * portafolio["contratos/titulos"] * 100
print(portafolio.T)

# Obtener Vega Total del Portafolio
vega_total = round(portafolio["vega_portafolio"].sum(), 4)
print(f"\nVega total del portafolio: {vega_total}")

# Calcula la vega ponderada por beta (beta-weighted vega)
def obtener_beta(ticker: str):
    
    """
    Función que obtiene la Beta del Activo desde Yahoo Finance.
    """
    
    # Generar Instancia
    asset = yf.Ticker(ticker=ticker)
    info = asset.info
    
    return info.get("beta", np.nan)

# Probar Funcionamiento
betas = [obtener_beta(ticker) for ticker in portafolio["activo"].iloc[:-1]]
betas.append(np.nan)
# Agregar Portafolio
portafolio["beta"] = betas
portafolio["beta_weighted_vega"] = portafolio["vega_portafolio"] * portafolio["beta"]
print(portafolio.T)

# Calcular la Vega ponderada del Portafolio
bwv = portafolio["beta_weighted_vega"].sum()
print("La vega ponderada por Beta es:", round(bwv, 4))

# Recordatorio:
#   - La Vega total mide la sensibilidad del portafolio a cambios en la volatilidad implícita, indicando
#     cómo variará su valor ante fluctuaciones en la volatilidad.
#   - La Vega Ponderada por Beta ajusta la sensibilidad a la volatilidad según la exposición sistemática
#     de cada activo, ayudando a entender y gestionar el impacto de cambios en la volatilidad a nive del mercado
#     en el portafolio diversificado.
