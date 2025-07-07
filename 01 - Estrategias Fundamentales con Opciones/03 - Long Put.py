# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la opción
precio_ejercicio = 100
prima_pagada = 10
precio_actual = 100

# Rango de precios al vencimiento
precios_finales = np.linspace(start=50, stop=150, num=300)

# Ganancia/Pérdida Long Put
beneficio_put = np.maximum(precio_ejercicio - precios_finales, 0) - prima_pagada

# Punto de equilibrio
punto_equilibrio = precio_ejercicio - prima_pagada

# Estilo oscuro
plt.style.use("dark_background")

# Crear gráfico
fig, ax = plt.subplots(figsize=(20, 8))

# Gráfico principal
ax.plot(precios_finales, beneficio_put, color="cyan", linewidth=2.5, linestyle="-", label="Ganancia/Pérdida Long Put")

# Rellenos de área de beneficios/pérdidas
ax.fill_between(x=precios_finales, y1=beneficio_put, y2=0, where=beneficio_put >= 0, color="cyan", alpha=0.25, 
                label="Zona de Ganancia")
ax.fill_between(x=precios_finales, y1=beneficio_put, y2=0, where=beneficio_put < 0, color="red", alpha=0.25, 
                label="Zona de Pérdida")

# Líneas de referencia
ax.axhline(y=0, color="white", linestyle="--", linewidth=1)
ax.axvline(x=precio_ejercicio, color="orange", linestyle="--", linewidth=1.5, label="Precio de Ejercicio")
ax.axvline(x=punto_equilibrio, color="magenta", linestyle=":", linewidth=1.5, label="Punto de Equilibrio")

# Anotaciones con flechas
ax.annotate("Ganancia Máxima = Strike - Prima", xy=(55, beneficio_put[10]), xytext=(72, 20),
            arrowprops=dict(arrowstyle="->", color="cyan"), color="cyan", fontsize=11)

ax.annotate(f"Pérdida Máxima = -${prima_pagada}", xy=(120, -prima_pagada + 0.5), xytext=(125, 3),
            arrowprops=dict(arrowstyle="->", color="red"), color="red", fontsize=11)

ax.annotate(f"Punto de Equilibrio = ${punto_equilibrio}", xy=(punto_equilibrio, 0), xytext=(punto_equilibrio - 2, 15),
            arrowprops=dict(arrowstyle="->", color="magenta"), color="magenta", fontsize=11)

ax.set_title("Estrategia Long Put - Visualización Estrategia", fontsize=16, color="white")
ax.set_xlabel("Precio del Activo Subyacente al Vencimiento", fontsize=12, color="white")
ax.set_ylabel("Ganancia/Pérdida", fontsize=12, color="white")

# Ajuste de ejes
ax.spines["bottom"].set_color("white")
ax.spines["left"].set_color("white")
ax.tick_params(axis="x", colors="white")
ax.tick_params(axis="y", colors="white")

ax.legend(loc="upper right", fontsize=11)
plt.grid()
plt.tight_layout()
plt.show()

# Resumen textual
print("\nRESUMEN ESTRATEGIA LONG PUT:\n")
print(f" - Precio de ejercicio: ${precio_ejercicio}")
print(f" - Prima pagada: ${prima_pagada}")
print(f" - Punto de Equilibrio: ${punto_equilibrio}")
print(f" - Pérdida Máxima: -${prima_pagada}")
print(f" - Ganancia Máxima: ${precio_ejercicio - prima_pagada} (si el precio llega a 0)")
print("- Se beneficia si el precio final < ${}".format(punto_equilibrio))

# Recordatorio:
#   - Un Long Put brinda el derecho a vender un activo a un precio fijo en el futuro, siendo ideal para beneficarse
#     ante caídas del mercado.
#   - La pérdida máxima es la prima pagada, mientras que la ganancia puede aumentar si el activo baja mucho. Esto la 
#     convierte en una estrategia bajista con riesgo controlado.
