# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import matplotlib.pyplot as plt

# Definir función para calcular la ganancia o pérdida de una opción individual al vencimiento
def payoff_option(tipo_opcion: str, strike: float, prima: float, cantidad_contratos: int,
                  posicion_opcion: str, precios_subyacente: np.array):
    
    """
    Calcula el perfil de ganancia/pérdida de una opción individual (call o put),
    considerando si es una posición larga o corta, y el número de contratos.
    """
    
    # Validar Tipo de Opción
    if tipo_opcion == "call":
        payoff = np.maximum(precios_subyacente - strike, 0) - prima
    elif tipo_opcion == "put":
        payoff = np.maximum(strike - precios_subyacente, 0) - prima
    else:
        raise ValueError("Tipo debe ser 'call' o 'put'")
        
    # Invertir el payoff si la posición es corta
    if posicion_opcion.lower() == "short":
        payoff = -payoff
        
    return payoff * cantidad_contratos * 100 # Total de Acciones en nuestra posición

# Definir función para obtener la ganancia o pérdida total de la posición
def estrategia_opciones(posiciones: list[dict], precios_subyacente: np.array):
    
    """
    Calcula el payoff total de una estrategia compuesta por múltiples posiciones en opciones.
    """
    
    # Definir un array para almacenar el payoff
    total_payoff = np.zeros_like(precios_subyacente)
    
    # Sumar el payoff de cada opción
    for pos in posiciones:
        # Obtener Beneficio para cada posición
        payoff = payoff_option(tipo_opcion=pos["tipo"], 
                               strike=pos["strike"], 
                               prima=pos["prima"], 
                               cantidad_contratos=pos["cantidad"],
                               posicion_opcion=pos["posicion"], 
                               precios_subyacente=precios_subyacente)
        # Ir acumulando el Beneficio de todas las posiciones
        total_payoff += payoff
        
    return total_payoff

# Definir función para graficar cada estrategia
def plot_payoff(precios_subyacente: np.array, payoff: np.array, titulo="Perfil de Ganancia/Pérdida"):
    
    """
    Grafica el perfil de g/p de una estrategia de opciones
    """
        
    # Generar figura
    plt.figure(figsize=(22, 6), dpi=300)
    
    # Plot Principal
    plt.plot(precios_subyacente, payoff, color="blue", lw=2, label="Ganancia/Pérdida")
    
    # Áreas de ganancia y pérdida coloreadas
    plt.fill_between(x=precios_subyacente, y1=payoff, y2=0, where=(payoff >= 0), color="green", alpha=0.3, label="Ganancia")
    plt.fill_between(x=precios_subyacente, y1=payoff, y2=0, where=(payoff < 0), color="red", alpha=0.3, label="Pérdida")
    
    plt.axhline(0, color="black", lw=1.2, linestyle="--")
    
    # Identificar máximos y mínimos
    x_max = precios_subyacente[np.argmax(payoff)]
    y_max = np.max(payoff)
    x_min = precios_subyacente[np.argmin(payoff)]
    y_min = np.min(payoff)
    
    # Anotaciones de máximos y mínimos
    plt.scatter([x_max], [y_max], color="darkgreen", s=80, zorder=5)
    plt.text(x=x_max, y=y_max, s=f"Máx: {y_max:.2f}", fontsize=12, fontweight="bold", color="darkgreen", verticalalignment="bottom")
    
    plt.scatter([x_min], [y_min], color="darkred", s=80, zorder=5)
    plt.text(x=x_min, y=y_min, s=f"Mín: {y_min:.2f}", fontsize=12, fontweight="bold", color="darkred", verticalalignment="top")
    
    # Ejes y título
    plt.xlabel("Precio del Subyacente al Vencimiento", fontsize=14)
    plt.ylabel("Ganancia / Pérdida", fontsize=14)
    plt.title(titulo, fontsize=16, fontweight="bold")
    
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()
    
# Rango de precios del subyacente para evaluar las estrategias
precios = np.linspace(start=50, stop=150, num=500)

# Ejemplo 1: Long Call - Se espera una fuerte subida en el subyacente
posiciones_1 = [{"tipo": "call", "strike": 100, "prima": 5, "cantidad": 1, "posicion": "long"}] # Long Call
payoff_1 = estrategia_opciones(posiciones=posiciones_1, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_1, titulo="Ejemplo 1: Long Call")
        
# Ejemplo 2: Long Put - Se espera una caída fuerte del subyacente
posiciones_2 = [{"tipo": "put", "strike": 100, "prima": 5, "cantidad": 1, "posicion": "long"}] # Long Put
payoff_2 = estrategia_opciones(posiciones=posiciones_2, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_2, titulo="Ejemplo 2: Long Put")
        
# Ejemplo 3: Bull Call Spread - Se espera una tendencia alcista, pero con riesgo limitado     
posiciones_3 = [{"tipo": "call", "strike": 100, "prima": 5, "cantidad": 1, "posicion": "long"}, # Long Call
                {"tipo": "call", "strike": 110, "prima": 2, "cantidad": 1, "posicion": "short"}, # Short Call
                ]
payoff_3 = estrategia_opciones(posiciones=posiciones_3, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_3, titulo="Ejemplo 3: Bull Call Spread")
                
# Ejemplo 4: Iron Condor - Gana con estabilidad; riesgo limitado si el precio se desvía       
posiciones_4 = [
    {"tipo": "put", "strike": 90, "prima": 1, "cantidad": 1, "posicion": "long"}, # Long Put
    {"tipo": "put", "strike": 95, "prima": 3, "cantidad": 1, "posicion": "short"}, # Short Put
    {"tipo": "call", "strike": 105, "prima": 3, "cantidad": 1, "posicion": "short"}, # Short Call
    {"tipo": "call", "strike": 110, "prima": 1, "cantidad": 1, "posicion": "long"}, # Long Call
                ]
payoff_4 = estrategia_opciones(posiciones=posiciones_4, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_4, titulo="Ejemplo 4: Iron Condor")
                        
# Ejemplo 5: Short Call - Estrategia bajista con riesgo limitado
posiciones_5 = [{"tipo": "call", "strike": 100, "prima": 5, "cantidad": 1, "posicion": "short"}] # Short Call
payoff_5 = estrategia_opciones(posiciones=posiciones_5, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_5, titulo="Ejemplo 5: Short Call")
                
# Ejemplo 6: Straddle - Estrategia para alta volatilidad (sin dirección clara)
posiciones_6 = [{"tipo": "call", "strike": 100, "prima": 5, "cantidad": 1, "posicion": "long"},
                {"tipo": "put", "strike": 100, "prima": 5, "cantidad": 1, "posicion": "long"}] 
payoff_6 = estrategia_opciones(posiciones=posiciones_6, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_6, titulo="Ejemplo 6: Straddle")
        
# Ejemplo 7: Butterfly Spread - Estrategia para baja volatilidad con beneficio limitado
posiciones_7 = [{"tipo": "call", "strike": 95, "prima": 7, "cantidad": 1, "posicion": "long"},
                {"tipo": "call", "strike": 100, "prima": 4, "cantidad": 2, "posicion": "short"},
                {"tipo": "call", "strike": 105, "prima": 2, "cantidad": 1, "posicion": "long"}] 
payoff_7 = estrategia_opciones(posiciones=posiciones_7, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_7, titulo="Ejemplo 7: Butterfly Spread con Calls")

# Ejemplo 8: Ratio Call Spread - Estrategia con sesgo bajista y crédito neto
posiciones_8 = [{"tipo": "call", "strike": 100, "prima": 8, "cantidad": 1, "posicion": "long"},
                {"tipo": "call", "strike": 110, "prima": 5, "cantidad": 2, "posicion": "short"}] 
payoff_8 = estrategia_opciones(posiciones=posiciones_8, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_8, titulo="Ejemplo 8: Ratio Call Spread")      

# Ejemplo 9: Backspread Call - Estrategia alcista agresiva para alta volatilidad
posiciones_9 = [{"tipo": "call", "strike": 100, "prima": 5, "cantidad": 1, "posicion": "short"},
                {"tipo": "call", "strike": 110, "prima": 2, "cantidad": 2, "posicion": "long"}] 
payoff_9 = estrategia_opciones(posiciones=posiciones_9, precios_subyacente=precios)
plot_payoff(precios_subyacente=precios, payoff=payoff_9, titulo="Ejemplo 9: Backspread Call")      
