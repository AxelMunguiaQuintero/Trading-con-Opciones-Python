# -*- coding: utf-8 -*-
# Importar l-ibrerías
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Parámetros de la Estrategia
stock_prices = np.linspace(start=50, stop=150, num=500)
strike_price = 100
premium = 5
initial_stock_price = 100

# Covered Call: long stock + short call -> Un Covered Call es una estrategia donde se posee un activo (como acciones)
# y se vende una opción call sobre ese mismo activo. Permite generar ingresos adicionales con la prima, pero limita
# las ganancias si el precio sube demasiado.
stock_profit = stock_prices - initial_stock_price
short_call_profit = premium - np.maximum(stock_prices - strike_price, 0)
covered_call_profit = stock_profit + short_call_profit

# Protective Put: long stock + long put -> Un Protective Put es una estrategia donde se compra un activo y simultáneamente
# una opción put. Protege contra caídas del precio, limitando pérdidas potenciales. Se utiliza como seguro, permitiendo 
# mantener el ctivo con un riesgo de pérdida controlado.
long_put_profit = np.maximum(strike_price - stock_prices, 0) - premium
protective_put_profit = stock_profit + long_put_profit

# Estilo de visualización
sns.set(style="whitegrid")
plt.rcParams.update(
    {
     "axes.edgecolor": "#333333",
     "figure.facecolor": "#f8f9fa"
     }
    )

# Gráfico
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(22, 8), dpi=300)

# Covered Call
axs[0].plot(stock_prices, stock_profit, "--", label="Acción", color="gray") # Beneficio/Pérdida de la acción
axs[0].plot(stock_prices, short_call_profit, "--", label="Venta de Call", color="orange") # B/P de la Opción
axs[0].plot(stock_prices, covered_call_profit, label="Covered Call", color="blue", lw=2) # B/P del Covered Call
axs[0].axhline(0, color="black", lw=0.8, linestyle="--")
# Añadir Título, Etiquetas y Anotaciones
axs[0].set_title("Estrategia Covered Call")
axs[0].set_xlabel("Precio del Subyacente al Vencimiento")
axs[0].set_ylabel("Ganancia/Pérdida")
axs[0].legend()
axs[0].annotate("Ganancia limitada\npor el Call Vendido", xy=(strike_price + 20, premium + 0.50),
                xytext=(strike_price + 25, 15), arrowprops=dict(arrowstyle="->", color="black"), fontsize=10)
axs[0].annotate("Pérdida igual a la acción\nsi baja el precio", xy=(70,-25),
                xytext=(80,-30), arrowprops=dict(arrowstyle="->", color="black"), fontsize=10)


# Protective Put
axs[1].plot(stock_prices, stock_profit, "--", label="Acción", color="gray") # Beneficio/Pérdida de la acción
axs[1].plot(stock_prices, long_put_profit, "--", label="Compra de Put", color="green") # B/P de la Opción
axs[1].plot(stock_prices, protective_put_profit, label="Protective Put", color="purple", lw=2) # B/P del Protective Put
axs[1].axhline(0, color="black", lw=0.8, linestyle="--")
# Añadir Título, Etiquetas y Anotaciones
axs[1].set_title("Estrategia Protective Put")
axs[1].set_xlabel("Precio del Subyacente al Vencimiento")
axs[1].set_ylabel("Ganancia/Pérdida")
axs[1].legend()
axs[1].annotate("Pérdida limitada\npor el Put Comprado", xy=(75, -25),
                xytext=(60, -15), arrowprops=dict(arrowstyle="->", color="black"), fontsize=10)
axs[1].annotate("Potencial alcista ilimitado", xy=(130, 25),
                xytext=(115, 30), arrowprops=dict(arrowstyle="->", color="black"), fontsize=10)

plt.suptitle("Visualización de Estrategias con Opciones", fontsize=20, color="#222222")
plt.tight_layout()
plt.show()

# Recordatorio:
#   - Covered Call: Ideal para inversionistas conservadores con acciones en cartera. Esta estrategia genera ingresos
#     adicionales mediante la venta de opciones call. Es rentable en mercados laterales o ligeramente alcistas,
#     ya que la prima recibida compensa una posible falta de grandes ganancias o estancamiento del activo.
#   - Protective Put: Esta estrategia actúa como un seguro para los inversionistas que poseen acciones, limitando
#     las pérdidas en caídas significativas del precio. Permite mantener la exposición al alza, mientras que la opción
#     put protege el capital frente a movimientos bajistas inesperados.
