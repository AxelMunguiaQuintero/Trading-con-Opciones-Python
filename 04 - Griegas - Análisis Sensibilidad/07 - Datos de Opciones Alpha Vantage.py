# Importar librerías
import yfinance as yf
from alpha_vantage.options import Options # pip install alpha-vantage
import matplotlib.pyplot as plt

# Crear Conexión con el Servidor
cliente = Options(key="API_KEY")
ticker = "SPY"
# Extraer todas las opciones disponibles
datos, _ = cliente.get_historical_options(symbol=ticker)

# Separar Calls y Puts
calls = datos[datos["type"] == "call"]
puts = datos[datos["type"] == "put"]

# Seleccionar una fecha
activo = yf.Ticker(ticker)
fecha_objetivo = activo.options[10]
precio_actual = activo.info["regularMarketPrice"]
calls = calls[calls["expiration"] == fecha_objetivo]
puts = puts[puts["expiration"] == fecha_objetivo]

# Lista de griegas y colores
griegas = ["delta", "gamma", "theta", "vega", "rho"]
colores = {
    
    "call": "#2a9d8f",
    "put": "#e76f51"
    
    }
simbolos = {
    
    "delta": chr(0x0394),
    "gamma": chr(0x0393),
    "theta": chr(0x0398),
    "vega": "Vega",
    "rho": chr(0x03C1)
    
    }

# Crear Subplots
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(22, 12), dpi=300)
axs = axs.ravel()
# Graficar las 5 Griegas
for i, griega in enumerate(griegas):
    # Graficar Datos
    axs[i].plot(calls["strike"].apply(float), calls[griega].apply(float), label=f"Call {simbolos[griega]}",
                color=colores["call"], lw=2)
    axs[i].plot(puts["strike"].apply(float), puts[griega].apply(float), label=f"Put {simbolos[griega]}",
                color=colores["put"], lw=2)
    # Añadir etiquetas
    axs[i].set_title(f"{simbolos[griega]} - Sensibilidad vs Strike", fontsize=12, fontweight="bold")
    axs[i].set_xlabel("Precio Strike")
    axs[i].set_ylabel(f"{simbolos[griega]}")
    axs[i].legend()
    axs[i].grid(True, linestyle="--", alpha=0.5)
    
# Último Subplot
axs[-1].axis("off")
axs[-1].text(x=0.5, y=0.5,
             s=f"Sensibilidades (Griegas) en Tiempo Real\npara opciones de {ticker}",
             fontsize=22,
             fontweight="bold",
             ha="center",
             va="center",
             bbox=dict(facecolor="lightgray", edgecolor="gray", boxstyle="round,pad=0.8"))

fig.suptitle(f"Griegas de Opciones - {ticker} - Expira {fecha_objetivo} - Precio: {precio_actual}", fontsize=16,
             fontweight="bold")
plt.tight_layout()
plt.show()

# Recordatorio:
#   - La librería de Alpha Vantage permite obtener datos de opciones, incluyendo las griegas, de forma muy sencilla y gratuita,
#     aunque con la limitación de 25 peticiones diarias.
