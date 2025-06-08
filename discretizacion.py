import pandas as pd

# Cargar el dataset original
dataset = pd.read_csv('datos_weatherbit_diarios.csv')

# Seleccionar las características óptimas
selected_features = ['clouds', 'precip', 'slp', 'solar_rad', 't_dni', 't_ghi', 'wind_dir', 'wind_gust_spd']
filtered_dataset = dataset[selected_features]

# Definir una función para discretizar variables numéricas con límites basados en datos científicos
def discretizar_variable(data, variable, bins, labels):
    data[variable + '_cat'] = pd.cut(data[variable], bins=bins, labels=labels, include_lowest=True)

# Definir los bins y labels en base a datos científicos para cada variable
bins_dict = {
    'clouds': [0, 30, 70, 100],           # Cobertura nubosa (%)
    'precip': [0, 2, 10, float('inf')],   # Precipitación (mm)
    'slp': [0, 1000, 1020, float('inf')], # Presión a nivel del mar (hPa)
    'solar_rad': [0, 200, 500, float('inf')],  # Radiación solar (W/m²)
    't_dni': [0, 300, 600, float('inf')],      # Radiación directa normal (W/m²)
    't_ghi': [0, 400, 700, float('inf')],      # Radiación global horizontal (W/m²)
    'wind_dir': [0, 90, 180, 270, 360],       # Dirección del viento (grados)
    'wind_gust_spd': [0, 5, 10, float('inf')] # Velocidad de ráfagas de viento (m/s)
}

labels_dict = {
    'clouds': ['bajo', 'medio', 'alto'],
    'precip': ['bajo', 'medio', 'alto'],
    'slp': ['bajo', 'medio', 'alto'],
    'solar_rad': ['bajo', 'medio', 'alto'],
    't_dni': ['bajo', 'medio', 'alto'],
    't_ghi': ['bajo', 'medio', 'alto'],
    'wind_dir': ['norte', 'este', 'sur', 'oeste'],  # Puntos cardinales
    'wind_gust_spd': ['bajo', 'medio', 'alto']
}

# Discretizar cada variable según los límites definidos
for feature, bins in bins_dict.items():
    labels = labels_dict[feature]
    discretizar_variable(filtered_dataset, feature, bins, labels)

# Crear un nuevo DataFrame con las variables discretizadas
categorical_features = [feature + '_cat' for feature in selected_features]
discretized_dataset = filtered_dataset[categorical_features]

# Exportar el nuevo dataset a un archivo CSV
output_path = 'datos_discretizados.csv'
discretized_dataset.to_csv(output_path, index=False)

print(f"El nuevo dataset con variables discretizadas ha sido guardado en: {output_path}")
