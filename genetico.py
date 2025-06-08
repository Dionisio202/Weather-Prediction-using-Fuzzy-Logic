import pandas as pd
import numpy as np
import random

# Parámetros de configuración
NUM_GENERACIONES = 100
TAMANO_POBLACION = 20
PROB_MUTACION = 40

# Función para crear un individuo (subconjunto de características)
def crear_individuo(num_features):
    return [random.choice([0, 1]) for _ in range(num_features)]

# Crear la población inicial
def crear_poblacion(tamano, num_features):
    return [crear_individuo(num_features) for _ in range(tamano)]

# Evaluar un individuo según la correlación promedio entre características seleccionadas
def evaluar_individuo(individuo, data):
    selected_features = [col for idx, col in enumerate(data.columns) if individuo[idx] == 1]

    if len(selected_features) < 6:
        return float('inf')  # Penaliza individuos con menos de 6 características

    # Calcular la correlación media entre las características seleccionadas
    selected_data = data[selected_features]
    correlation_matrix = selected_data.corr().abs()

    # Usar solo la parte superior de la matriz de correlación sin la diagonal
    upper_triangle_indices = np.triu_indices_from(correlation_matrix, k=1)
    correlations = correlation_matrix.values[upper_triangle_indices]

    # Filtrar valores NaN de las correlaciones y calcular el promedio
    correlations = correlations[~np.isnan(correlations)]
    if len(correlations) == 0:
        return float('inf')  # Penaliza si no hay correlaciones válidas

    avg_correlation = correlations.mean()

    # El fitness es directamente proporcional a la media de la correlación (queremos minimizarla)
    return avg_correlation

# Selección de padres basada en probabilidades inversas de evaluación
def seleccionar_padres(poblacion, evaluaciones):
    valid_evaluations = [1/eval if np.isfinite(eval) and eval != 0 else 0 for eval in evaluaciones]

    if sum(valid_evaluations) == 0:
        raise ValueError("Todos los individuos tienen evaluaciones no finitas o cero. Verifica la función de evaluación.")

    padres = random.choices(poblacion, weights=valid_evaluations, k=2)
    return padres[0], padres[1]

# Cruza dos padres para generar hijos
def cruzar_padres(padre1, padre2):
    punto_cruce = random.randint(1, len(padre1) - 2)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2

# Mutación: cambia un gen aleatoriamente
def mutar(individuo):
    idx = random.randint(0, len(individuo) - 1)
    individuo[idx] = 1 - individuo[idx]
    return individuo

# Algoritmo Genético
def algoritmo_genetico(data):
    num_features = data.shape[1]
    poblacion = crear_poblacion(TAMANO_POBLACION, num_features)
    historial_mejores = []

    for generacion in range(NUM_GENERACIONES):
        evaluaciones = [evaluar_individuo(ind, data) for ind in poblacion]

        # Guarda el mejor individuo de la generación
        mejor_indice = np.argmin(evaluaciones)
        mejor_individuo = poblacion[mejor_indice]
        mejor_puntaje = evaluaciones[mejor_indice]
        mejores_caracteristicas = [data.columns[i] for i, val in enumerate(mejor_individuo) if val == 1]
        historial_mejores.append((mejores_caracteristicas, mejor_puntaje))

        nueva_poblacion = []
        while len(nueva_poblacion) < TAMANO_POBLACION:
            padre1, padre2 = seleccionar_padres(poblacion, evaluaciones)
            hijo1, hijo2 = cruzar_padres(padre1, padre2)

            # Mutación con probabilidad
            if random.random() < PROB_MUTACION / 100:
                hijo1 = mutar(hijo1)
            if random.random() < PROB_MUTACION / 100:
                hijo2 = mutar(hijo2)

            nueva_poblacion.extend([hijo1, hijo2])

        poblacion = nueva_poblacion[:TAMANO_POBLACION]

    # Mejor puntaje final
    mejor_individuo_final, mejor_puntaje_final = min(historial_mejores, key=lambda x: x[1])
    return historial_mejores[-10:], mejor_individuo_final, mejor_puntaje_final

# Cargar y preparar el dataset
dataset = pd.read_csv('datos_weatherbit_diarios.csv')

# Excluir columnas innecesarias
exclude_columns = ['max_temp_ts', 'min_temp_ts', 'datetime', 'ts', 'max_wind_spd_ts', 'lat', 'lon']
dataset_features = dataset.drop(columns=[col for col in exclude_columns if col in dataset.columns])
dataset_features = dataset_features.select_dtypes(include=[np.number])  # Mantiene solo las columnas numéricas

# Ejecutar el algoritmo genético en el dataset
mejores_10_resultados, mejor_individuo_final, mejor_puntaje_final = algoritmo_genetico(dataset_features)

# Mostrar los 10 mejores puntajes y sus características de las generaciones anteriores
print("Últimos 10 mejores puntajes por generación:")
for idx, (caracteristicas, puntaje) in enumerate(mejores_10_resultados, start=1):
    print(f"Generación {idx} - Mejores características: {caracteristicas} - Puntaje (correlación promedio): {puntaje}")

# Mostrar el mejor puntaje final
print("\nMejor puntaje final:")
print(f"Mejores características: {mejor_individuo_final}")
print(f"Mejor puntaje (correlación promedio): {mejor_puntaje_final}")
