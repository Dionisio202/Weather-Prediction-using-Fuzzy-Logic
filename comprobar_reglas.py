# Let's load the dataset and verify if the rule indeed holds across all rows.
import pandas as pd

# Cargar el dataset
file_path = 'datos_weatherbit_diarios.csv'
dataset = pd.read_csv(file_path)

# Definir las columnas del antecedente y el consecuente
antecedent_columns = ['wind_spd', 'wind_dir', 'pres']
consequent_columns = ['temp', 't_ghi']

# Verificar la presencia de valores para el antecedente y el consecuente en cada fila
antecedent_presence = dataset[antecedent_columns].notna().all(axis=1)
consequent_presence = dataset[consequent_columns].notna().all(axis=1)

# Verificar si todas las filas con el antecedente también tienen el consecuente
rule_holds = (antecedent_presence & consequent_presence).all()

# Imprimir los resultados
print("¿La regla se sostiene en todo el dataset?:", rule_holds)
print("¿El antecedente está presente en todas las filas?:", antecedent_presence.all())
print("¿El consecuente está presente en todas las filas?:", consequent_presence.all())
