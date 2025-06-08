import pandas as pd
from itertools import combinations

# Cargar el dataset discretizado
dataset = pd.read_csv('datos_discretizados.csv')

# Crear una lista de transacciones
transactions = []

for index, row in dataset.iterrows():
    transaction = set()
    for col in dataset.columns:
        item = f"{col}_{row[col]}"
        transaction.add(item)
    transactions.append(transaction)

# Calcular la cobertura de un antecedente
def calcular_cobertura(antecedente, transactions):
    return sum(1 for transaction in transactions if antecedente.issubset(transaction))

# Verificar cuántas veces el consecuente aparece en las mismas transacciones del antecedente
def verificar_consecuente(antecedente, consecuente, transactions):
    return sum(1 for transaction in transactions if antecedente.issubset(transaction) and consecuente.issubset(transaction))

# Calcular soporte, confianza y lift
def calcular_metricas(antecedente, consecuente, transactions):
    total_transactions = len(transactions)
    
    # Calcular soporte
    soporte_antecedente = calcular_cobertura(antecedente, transactions) / total_transactions
    soporte_consecuente = calcular_cobertura(consecuente, transactions) / total_transactions
    soporte_regla = verificar_consecuente(antecedente, consecuente, transactions) / total_transactions
    
    # Calcular confianza
    confianza = soporte_regla / soporte_antecedente if soporte_antecedente > 0 else 0
    
    # Calcular lift
    lift = confianza / soporte_consecuente if soporte_consecuente > 0 else 0
    
    return soporte_regla, confianza, lift

# Obtener todas las categorías de 'solar_rad_cat' y 'clouds_cat'
consecuente_variables = ['precip_cat']
consecuente_productos = set()

for transaction in transactions:
    for item in transaction:
        var_name = '_'.join(item.split('_')[:-1])  # Obtener el nombre de la variable
        if var_name in consecuente_variables:
            consecuente_productos.add(item)

# Generar reglas con las características categorizadas
def generar_reglas_complejas(transactions, consecuente_productos, min_soporte=0.5, min_confianza=0.5, max_antecedente_size=3):
    productos = set(item for transaction in transactions for item in transaction)
    productos_antecedente = productos - consecuente_productos  # Excluir los productos del consecuente
    reglas_validas = []
    
    for antecedente_size in range(1, max_antecedente_size + 1):
        for antecedente_combo in combinations(productos_antecedente, antecedente_size):
            antecedente = set(antecedente_combo)
            soporte_antecedente = calcular_cobertura(antecedente, transactions) / len(transactions)
            
            if soporte_antecedente >= min_soporte:
                for consecuente in consecuente_productos:
                    if consecuente not in antecedente:
                        consecuente_set = set([consecuente])
                        soporte_regla, confianza, lift = calcular_metricas(antecedente, consecuente_set, transactions)
                        
                        if soporte_regla >= min_soporte and confianza >= min_confianza and lift > 1:
                            regla = {
                                'antecedente': antecedente,
                                'consecuente': consecuente_set,
                                'soporte': soporte_regla,
                                'confianza': confianza,
                                'lift': lift
                            }
                            reglas_validas.append(regla)
    return reglas_validas

# Generar reglas
reglas = generar_reglas_complejas(transactions, consecuente_productos, min_soporte=0.01, min_confianza=0.01)

# Guardar las reglas en un archivo .txt y mostrar el número total de reglas
output_path = 'reglas_generadas.txt'
with open(output_path, 'w') as file:
    for regla in reglas:
        antecedente = ', '.join(regla['antecedente'])
        consecuente = ', '.join(regla['consecuente'])
        file.write(f"Regla: Si {antecedente} entonces {consecuente}\n")
        file.write(f"Soporte: {regla['soporte']:.2f}, Confianza: {regla['confianza']:.2f}, Lift: {regla['lift']:.2f}\n")
        file.write("-----\n")
    file.write(f"\nNúmero total de reglas generadas: {len(reglas)}\n")

print(f"Archivo generado en: {output_path}")
