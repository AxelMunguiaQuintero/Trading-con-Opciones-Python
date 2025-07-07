# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt

# Parámetros de la Opción
precio_ejercicio = 100
prima_pagada = 10 
precio_actual = 100

# Rango de precios simulados al vencimiento
precios_finales = np.linspace(start=precio_actual * 0.5, stop=precio_actual * 1.5, num=200)

# Cálculo del beneficio
beneficio_call = np.maximum(precios_finales - precio_ejercicio, 0) - prima_pagada

# Punto de equilibrio
punto_equilibrio = precio_ejercicio + prima_pagada

# Visualización
plt.figure(figsize=(22, 8))
plt.plot(precios_finales, beneficio_call, label="Ganancia/Pérdida Long Call", color="green", linewidth=2)

# Agregar niveles de información importantes
plt.axhline(y=0, color="black", linestyle="--")
plt.axvline(x=precio_ejercicio, color="blue", linestyle="--", linewidth=1.5, label="Precio de Ejercicio")
plt.axvline(x=punto_equilibrio, color="purple", linestyle="--", linewidth=1.5, label="Punto de Equilibrio")

# Relleno entre zonas (Identificar áreas de pérdida y beneficio)
plt.fill_between(x=precios_finales, y1=beneficio_call, y2=0, where=beneficio_call >= 0, color="green", alpha=0.3)
plt.fill_between(x=precios_finales, y1=beneficio_call, y2=0, where=beneficio_call < 0, color="red", alpha=0.3)

# Anotaciones clave en el plot
plt.scatter([punto_equilibrio], [0], color="purple", zorder=5, s=50)
plt.annotate(f"Punto de Equilibrio:\n${punto_equilibrio:.2f}", xy=(punto_equilibrio + 0.10, 0.5),
             xytext=(punto_equilibrio+3, 10), arrowprops=dict(headwidth=10, headlength=10, color="purple"), fontsize=10,
             fontstyle="italic", color="purple")
plt.annotate(f"Pérdida Máxima\n-${prima_pagada}", xy=(precio_ejercicio - 20, -prima_pagada + 1), fontsize=10, color="darkred")

plt.title("Estrategia Long Call - Opciones Financieras", fontsize=16)
plt.xlabel("Precio del Activo Subyacente al Vencimiento", fontsize=12)
plt.ylabel("Ganancia/Pérdida", fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Resumen Textual
print("\nRESUMEN ESTRATEGIA LONG CALL")
print(f" - Precio de Ejercicio: ${precio_ejercicio}")
print(f" - Prima pagada: ${prima_pagada}")
print(f" - Punto de equilibrio: ${punto_equilibrio}")
print(f" - Pérdida máxima: -${prima_pagada}")
print(" - Ganancia máxima: ilimitada")
print(f" - Se beneficia si el precio final > ${precio_ejercicio}")

# Recordatorio:
#   - Un Long Call otorga el derecho, pero no la obligación, de comprar un activo a un precio fijo, buscando
#     beneficiarse de subidas significativas en su precio durante un periodo determinado.
#   - El riesgo máximo se limita a la prima pagada por la opción, mientras que el beneficio potencial es ilimitado,
#     lo que la hace atractiva para inversores/traders con perspectivas alcistas.
#   - El punto de equilibrio es el precio de ejercicio más la prima; solo se obtienen ganancias si el precio del activo
#     supera este nivel.
