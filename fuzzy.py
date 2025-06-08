from flask import Flask, render_template, request, send_file
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import io
import re
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Diccionarios para la clasificación
bins_dict = {
    'clouds': [0, 30, 70, 100],
    'precip': [0, 2, 10, float('inf')],
    'slp': [0, 1000, 1020, float('inf')],
    'solar_rad': [0, 200, 500, float('inf')],
    't_dni': [0, 300, 600, float('inf')],
    't_ghi': [0, 400, 700, float('inf')],
    'wind_dir': [0, 90, 180, 270, 360],
    'wind_gust_spd': [0, 5, 10, float('inf')]
}

labels_dict = {
    'clouds': ['bajo', 'medio', 'alto'],
    'precip': ['bajo', 'medio', 'alto'],
    'slp': ['bajo', 'medio', 'alto'],
    'solar_rad': ['bajo', 'medio', 'alto'],
    't_dni': ['bajo', 'medio', 'alto'],
    't_ghi': ['bajo', 'medio', 'alto'],
    'wind_dir': ['norte', 'este', 'sur', 'oeste'],
    'wind_gust_spd': ['bajo', 'medio', 'alto']
}

# Función para categorizar valores numéricos
def categorize_value(value, variable_name):
    base_variable_name = variable_name.replace('_cat', '')
    bins = bins_dict[base_variable_name]
    labels = labels_dict[base_variable_name]
    category = pd.cut([value], bins=bins, labels=labels, right=False)[0]
    return category

# Paso 1: Cargar el dataset discretizado
dataset = pd.read_csv('datos_discretizados.csv')

# Definir variables de salida
output_features = ['precip_cat']

# Inicializar conjunto de variables utilizadas en las reglas
variables_en_reglas = set()

# Leer y procesar reglas desde el archivo 'reglas_generadas.txt'
with open('reglas_generadas.txt', 'r', encoding='latin-1') as file:
    lines = file.readlines()

for i in range(0, len(lines), 3):
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
    
    variables_difusas[output_feature].defuzzify_method = 'centroid'
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

# Diccionario de nombres amigables para las variables
friendly_names = {
    'clouds_cat': 'Nubosidad',
    'solar_rad_cat': 'Radiación Solar',
    'wind_dir_cat': 'Dirección del Viento',
    'slp_cat': 'Presión Atmosférica',
    'wind_gust_spd_cat': 'Ráfagas de Viento',
    't_dni_cat': 'Radiación Directa',
    't_ghi_cat': 'Irradiación Horizontal',
    'precip_cat': 'Precipitación'
}
units_dict = {
    'clouds_cat': '%',
    'solar_rad_cat': 'W/m²',
    'wind_dir_cat': 'grados',
    'slp_cat': 'hPa',
    'wind_gust_spd_cat': 'm/s',
    't_dni_cat': 'W/m²',
    't_ghi_cat': 'W/m²'
}

@app.route('/')
def index():
    return render_template('index.html', input_features=input_features, friendly_names=friendly_names, units_dict=units_dict)

@app.route('/procesar', methods=['POST'])
def procesar():
    entrada = {}
    for feature in input_features:
        valor = request.form[feature]
        entrada[feature] = valor
        if feature == 'wind_dir_cat':
            if valor == 'norte':
                input_value = 0
            elif valor == 'este':
                input_value = 90
            elif valor == 'sur':
                input_value = 180
            elif valor == 'oeste':
                input_value = 270
        else:
            valor = float(valor)
            categoria = categorize_value(valor, feature)
            input_value = 0 if categoria == 'bajo' else 1 if categoria == 'medio' else 2
        for simulation in simulations.values():
            simulation.input[feature] = input_value

    resultados = {}
    for output_feature, simulation in simulations.items():
        simulation.compute()
        resultado = simulation.output[output_feature]

        output_variable = variables_difusas[output_feature]
        grado_bajo = fuzz.interp_membership(output_variable.universe, output_variable['bajo'].mf, resultado)
        grado_medio = fuzz.interp_membership(output_variable.universe, output_variable['medio'].mf, resultado)
        grado_alto = fuzz.interp_membership(output_variable.universe, output_variable['alto'].mf, resultado)

        interpretacion = (
            'bajo' if grado_bajo >= grado_medio and grado_bajo >= grado_alto else
            'medio' if grado_medio >= grado_bajo and grado_medio >= grado_alto else
            'alto'
        )

        resultados[output_feature] = {
            'valor_numerico': resultado,
            'interpretacion': interpretacion,
            'grado_pertenencia': max(grado_bajo, grado_medio, grado_alto)
        }

    return render_template('resultado.html', entrada=entrada, resultados=resultados, friendly_names=friendly_names, units_dict=units_dict)

@app.route('/grafico')
def grafico():
    fig, axes = plt.subplots(len(variables_difusas), 1, figsize=(8, len(variables_difusas) * 3))
    fig.tight_layout(pad=4.0)
    
    for idx, (name, variable) in enumerate(variables_difusas.items()):
        ax = axes[idx] if len(variables_difusas) > 1 else axes
        for label in variable.terms:
            ax.plot(variable.universe, variable[label].mf, label=label.capitalize())
        ax.set_title(f'Función de Pertenencia para {name}')
        ax.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype='image/png')

# Agregar ruta para visualizar la agregación y defuzzificación
@app.route('/grafico_aggregacion')
def grafico_aggregacion():
    output_feature = output_features[0]
    fig, ax = plt.subplots(figsize=(8, 4))
    variables_difusas[output_feature].view(sim=simulations[output_feature], ax=ax)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
