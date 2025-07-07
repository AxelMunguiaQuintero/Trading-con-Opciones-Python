# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Descargar Datos
activo = "AAPL"
inicio = "2020-01-01"
fin = "2025-01-01"
datos = yf.download(tickers=activo, start=inicio, end=fin, multi_level_index=False, interval="1d")

# Calcular Rendimientos
datos["Retornos"] = datos["Close"].pct_change()

# Eliminar los valores nulos
datos.dropna(inplace=True)

# Calcular Volatilidad Histórica
vol_diaria = datos["Retornos"].std()
vol_anual = vol_diaria * np.sqrt(252)

print(f"Volatilidad diaria: {vol_diaria:.4f}\n")
print(f"Volatilidad anualizada: {vol_anual:.4f}")

# Crear una figura para mostrar la evolución del precio y la volatilidad
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(22, 12))

# Gráfico 1: Precios de Cierre
axes[0].plot(datos.index, datos["Close"], label="Precios de Cierre", color="royalblue")
axes[0].set_title(f"Evolución del Precio de {activo}")
axes[0].set_ylabel("Precio ($)")
axes[0].grid()
axes[0].legend()

# Gráfico 2: Retornos Diarios
axes[1].plot(datos.index, datos["Retornos"], label="Retornos Diarios", color="orange")
axes[1].set_title("Retornos Diarios")
axes[1].set_ylabel("Retorno")
axes[1].axhline(0, color="black", linestyle="--", lw=0.8)
axes[1].grid()
axes[1].legend()

# Gráfico 3: Volatilidad Móvil
ventana = 21 # Aprox. un mes de trading (252 / 12 = 21)
datos["Volatilidad_21d"] = datos["Retornos"].rolling(window=ventana, min_periods=ventana).std() * np.sqrt(252)
axes[2].plot(datos.index, datos["Volatilidad_21d"], label=f"Volatilidad Anualizada ({ventana} días)", color="crimson")
axes[2].set_title("Volatilidad Anualizada Móvil")
axes[2].set_ylabel("Volatilidad")
axes[2].grid()
axes[2].legend()

plt.tight_layout()
plt.show()

# Comparar la volatilidad para diferentes marcos de tiempo (1 minuto, 1 hora, 1 dí, 1 semana)
intervalos = {
    
    # Clave: (Intervalo, Periodo a descargar, Valor a utilizar para anualizar la volatilidad)
    "1m": ("1 Minuto", "7d", 252 * 6.5 * 60), # 252 días * 6.5 horas * 60 minutos = Minutos activos de trading anuales
    "60m": ("60 Minutos", "60d", 252 * 6.5),  # 252 días * 6.5 (una hora por barra) 
    "1d": ("1 Día", "1y", 252),               # 252 días hábiles por año
    "1wk": ("1 Semana", "3y", 52)             # 52 Semanas por año
    
    }

# Definir una variable para guardar las volatilidades
volatilidades = {}

# Iterar en cada intervalo para descargar los datos y calcular las volatilidades
for intervalo, (nombre, periodo, factor) in intervalos.items():
    # Descargos Datos
    try:
        df = yf.download(activo, period=periodo, interval=intervalo, multi_level_index=False)
        df["Retornos"] = df["Close"].pct_change()
        vol = df["Retornos"].std() * np.sqrt(factor)
        volatilidades[nombre] = vol
        print(f"{nombre:<10} -> Volatilidad Anualizada {vol:.4f}")
    except Exception:
        print(f"{nombre:<10} -> Error al descargar o procesar los datos") 

# Visualización
plt.figure(figsize=(10, 5))
sns.barplot(x=list(volatilidades.keys()), y=list(volatilidades.values()), palette="crest")
plt.title("Comparación de Volatilidad Anualizada")
plt.ylabel("Volatilidad")
plt.xlabel("Intervalo")
plt.grid(axis="y", linestyle="--", alpha=0.8)
plt.tight_layout()
plt.show()

# Recordatorio:
#   - La Volatilidad Histórica mide la dispersión de los rendimientos pasados de un activo, y es calculada como la desviación
#     estándar de sus rendimientos en un periodo determinado, reflejando el riesgo y la incertidumbre del mercado.
#   - Para calcular la volatilidad en distintas ventanas de tiempo, se tiene que considerar la cantidad total de unidades
#     temporales involucradas -ya sean minutos, horas, días o semanas- para escalar correctamente la desviación estándar
#     al periodo anual.
