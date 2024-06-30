import pandas as pd
import joblib

def process_workload(data):
    #def process_data_workload():
    data = data.dropna()

    #clf = joblib.load("Workload_DTree_model_150.joblib")
    clf = joblib.load("Workload/Workload_LSVR_model.joblib")

    predicciones = clf.predict(data)

    # Crear un DataFrame de pandas con las predicciones
    df_predicciones = pd.DataFrame(predicciones, columns=['Workload'])

    replicas = 8

    # Crear una lista para almacenar las filas replicadas
    replicated_rows = []

    # Iterar sobre cada fila del DataFrame original
    for _, row in df_predicciones.iterrows():
        # Añadir la fila replicada 8 veces a la lista
        for _ in range(replicas):
            replicated_rows.append(row)

    # Convertir la lista de filas replicadas en un DataFrame
    df_repetido = pd.DataFrame(replicated_rows, columns=df_predicciones.columns)

    # Guardar el DataFrame en un archivo CSV
    df_repetido.to_csv('Workload/predicciones_LSVR_prueba.csv', index=False)

    return df_repetido