import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import re

# Paso 1: Cargar el dataset discretizado
dataset = pd.read_csv('datos_discretizados.csv')

# Definir variables de salida
output_features = ['precip_cat']

# Inicializar conjunto de variables utilizadas en las reglas
variables_en_reglas = set()

# Paso 3: Leer y procesar reglas desde el archivo 'reglas_generadas.txt'
with open('reglas_generadas.txt', 'r', encoding='latin-1') as file:
    lines = file.readlines()

for i in range(0, len(lines), 3):  # Cada regla ocupa 3 líneas
    regla_line = lines[i].strip()
    if not regla_line.startswith('Regla:'):
        continue
    match = re.match(r"Regla: Si (.+) entonces (.+)", regla_line)
    if match:
        antecedente_str, consecuente_str = match.groups()
        for term in antecedente_str.strip().split(', '):
            var_name, membership_value = term.rsplit('_', 1)
            variables_en_reglas.add(var_name)
            
input_features = list(variables_en_reglas)
print("Variables de entrada:", input_features)

# Definir variables difusas
variables_difusas = {}
for feature in input_features:
    if feature == 'wind_dir_cat':
        universe = np.array([0, 90, 180, 270, 360])
        variables_difusas[feature] = ctrl.Antecedent(universe, feature)
        variables_difusas[feature]['norte'] = fuzz.trimf(universe, [-45, 0, 45])
        variables_difusas[feature]['este'] = fuzz.trimf(universe, [45, 90, 135])
        variables_difusas[feature]['sur'] = fuzz.trimf(universe, [135, 180, 225])
        variables_difusas[feature]['oeste'] = fuzz.trimf(universe, [225, 270, 315])
    else:
        universe = np.array([0, 1, 2])
        variables_difusas[feature] = ctrl.Antecedent(universe, feature)
        variables_difusas[feature]['bajo'] = fuzz.trimf(universe, [-1, 0, 1])
        variables_difusas[feature]['medio'] = fuzz.trimf(universe, [0, 1, 2])
        variables_difusas[feature]['alto'] = fuzz.trimf(universe, [1, 2, 3])

for output_feature in output_features:
    universe = np.linspace(0, 100, 100)
    variables_difusas[output_feature] = ctrl.Consequent(universe, output_feature)
    variables_difusas[output_feature]['bajo'] = fuzz.trimf(universe, [0, 0, 40])
    variables_difusas[output_feature]['medio'] = fuzz.trimf(universe, [30, 50, 70])
    variables_difusas[output_feature]['alto'] = fuzz.trimf(universe, [60, 100, 100])

print("Variables difusas definidas:", list(variables_difusas.keys()))

# Procesar reglas
fuzzy_rules = []
with open('reglas_generadas.txt', 'r', encoding='latin-1') as file:
    lines = file.readlines()

for i in range(0, len(lines), 3):
    regla_line = lines[i].strip()
    if not regla_line.startswith('Regla:'):
        continue
    match = re.match(r"Regla: Si (.+) entonces (.+)", regla_line)
    if match:
        antecedente_str, consecuente_str = match.groups()
        antecedente_terms = []
        for term in antecedente_str.strip().split(', '):
            var_name, membership_value = term.rsplit('_', 1)
            if var_name in variables_difusas:
                variable = variables_difusas[var_name]
                antecedente_terms.append(variable[membership_value])
        if not antecedente_terms:
            continue
        combined_antecedent = antecedente_terms[0]
        for term in antecedente_terms[1:]:
            combined_antecedent &= term
        consecuente_terms = []
        for term in consecuente_str.strip().split(', '):
            var_name, membership_value = term.rsplit('_', 1)
            if var_name in output_features:
                variable = variables_difusas[var_name]
                consecuente_terms.append(variable[membership_value])
        if not consecuente_terms:
            continue
        combined_consequent = consecuente_terms[0]
        rule = ctrl.Rule(combined_antecedent, combined_consequent)
        fuzzy_rules.append(rule)

if not fuzzy_rules:
    print("No se han generado reglas difusas. Verifica que las reglas estén correctamente definidas.")
    exit()

# Crear sistemas de control difuso
control_systems = {}
simulations = {}
for output_feature in output_features:
    rules_for_output = [rule for rule in fuzzy_rules if rule.consequent[0].term.parent.label == output_feature]
    if not rules_for_output:
        print(f"No hay reglas para la variable de salida '{output_feature}'.")
        continue
    control_system = ctrl.ControlSystem(rules_for_output)
    simulation = ctrl.ControlSystemSimulation(control_system)
    control_systems[output_feature] = control_system
    simulations[output_feature] = simulation

entrada = {
    'clouds_cat': 'alto',          # Nubosidad máxima.
    'solar_rad_cat': 'bajo',       # Radiación solar baja, indicando nubes densas.
    'wind_dir_cat': 'sur',        # Cambiar dirección del viento a este, que puede traer humedad.
    'slp_cat': 'bajo',             # Muy baja presión, aumentando la probabilidad de tormenta.
    'wind_gust_spd_cat': 'alto',   # Viento fuerte, característico de sistemas de tormenta.
    't_dni_cat': 'bajo',           # Radiación directa baja, cielo nublado.
    't_ghi_cat': 'bajo'            # Baja irradiación horizontal, poca penetración de luz solar.
}



print("Valores de entrada:", entrada)

for feature in input_features:
    categoria = entrada.get(feature, 'medio')
    if feature == 'wind_dir_cat':
        input_value = 0 if categoria == 'norte' else 90 if categoria == 'este' else 180 if categoria == 'sur' else 270
    else:
        input_value = 0 if categoria == 'bajo' else 1 if categoria == 'medio' else 2
    for simulation in simulations.values():
        simulation.input[feature] = input_value

# Ejecutar simulaciones y verificar si `precip_cat` tiene una salida generada
for output_feature, simulation in simulations.items():
    simulation.compute()
    if output_feature in simulation.output:
        resultado = simulation.output[output_feature]
        print(f"Valor de salida ({output_feature}): {resultado}")
        output_variable = variables_difusas[output_feature]
        grado_bajo = fuzz.interp_membership(output_variable.universe, output_variable['bajo'].mf, resultado)
        grado_medio = fuzz.interp_membership(output_variable.universe, output_variable['medio'].mf, resultado)
        grado_alto = fuzz.interp_membership(output_variable.universe, output_variable['alto'].mf, resultado)
        interpretacion = 'bajo' if grado_bajo >= grado_medio and grado_bajo >= grado_alto else 'medio' if grado_medio >= grado_bajo and grado_medio >= grado_alto else 'alto'
        if output_feature == 'precip_cat':
            print(f"El valor de la Precipitacion es '{interpretacion}' con un grado de pertenencia de {max(grado_bajo, grado_medio, grado_alto):.2f}")
        else:
            print(f"El valor de '{output_feature}' es '{interpretacion}' con un grado de pertenencia de {max(grado_bajo, grado_medio, grado_alto):.2f}")
    else:
        print(f"No se generó ninguna salida para '{output_feature}'. Verifica las reglas y las condiciones de entrada.")
