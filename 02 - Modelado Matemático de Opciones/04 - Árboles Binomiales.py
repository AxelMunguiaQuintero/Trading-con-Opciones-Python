# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np

# Definir función utilizando Árboles Binomiales
def arbol_binomial_opciones(S, K, T, r, sigma, n, tipo="europea", opcion="call"):
    
    """
    Calcula el precio de una opción usando árboles binomiales.
    """
    
    # Definir parámetros
    dt = T / n # Tamaño de cada paso
    u = np.exp(sigma * np.sqrt(dt)) # Factor de Subida
    d = 1 / u # Factor de bajada
    p = (np.exp(r * dt) - d) / (u - d) # Probabilidad neutral al riesgo
    
    # Inicializar matriz de precios del activo
    arbol = np.zeros((n + 1, n + 1))
    arbol[0, 0] = S
    
    # Construir árbol de precios del activo
    for i in range(1, n+1):
        for j in range(0, i + 1):
            arbol[i, j] = 100 * u ** (i - j) * d ** j
            
    # Calcular payoff en el último nodo
    payoff = np.zeros((n + 1, n + 1))
    for j in range(n + 1):
        if opcion == "call":
            # Revisar en el último paso en todos los nodos
            payoff[n, j] = max(0, arbol[n, j] - K)
        else:
            # Revisar en el último paso en todos los nodos
            payoff[n, j] = max(0, K - arbol[n, j])
            
    # Retropropagación: Retroceder en el árbol
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            # Calcular Función del Valor de Continuar
            payoff[i, j] = np.exp(-r * dt) * (p * payoff[i + 1, j] + (1 - p) * payoff[i + 1, j + 1])
            
            # Extender fórmula para Opciones Americanas
            if tipo == "americana":
                if opcion == "call":
                    ejercicio = max(0, arbol[i, j] - K)
                else:
                    ejercicio = max(0, K - arbol[i, j])
                payoff[i, j] = max(payoff[i, j], ejercicio)
            
            
    return payoff[0, 0]
            

# Ejemplo de Uso
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.20
n = 1_000

# Opción Europea Call
call_europea = arbol_binomial_opciones(S=S, K=K, T=T, r=r, sigma=sigma, n=n, tipo="europea", opcion="call")
print(f"Call Europea: {call_europea:.2f}")

# Opción Europea Put
put_europea = arbol_binomial_opciones(S=S, K=K, T=T, r=r, sigma=sigma, n=n, tipo="europea", opcion="put")
print(f"Put Europea: {put_europea:.2f}")

# Opción Americana Call
call_americana = arbol_binomial_opciones(S=S, K=K, T=T, r=r, sigma=sigma, n=n, tipo="americana", opcion="call")
print(f"Call Americano: {call_americana:.2f}")

# Opción Americana Put
put_americana = arbol_binomial_opciones(S=S, K=K, T=T, r=r, sigma=sigma, n=n, tipo="americana", opcion="put")
print(f"Put Americano: {put_americana:.2f}")

# Recordatorio:
#   - Los árboles binomiales permiten valorar opciones europeas y americanas, ya que modelan paso a paso
#     la evolución del precio del activo subyacente, facilitando la incorporación de la posibilidad de ejercer
#     anticipadamente en americanas.
