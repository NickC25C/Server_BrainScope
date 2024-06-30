import pandas as pd
import joblib
#def process_data_memorization():
data = pd.read_csv('ProcessData.csv')
data = data.dropna()

#clf = joblib.load("Memorization_DTree_model_150.joblib")
clf = joblib.load("Memorization_LSVR_model.joblib")

predicciones = clf.predict(data)

# Crear un DataFrame de pandas con las predicciones
df_predicciones = pd.DataFrame(predicciones, columns=['Predicción'])

# Guardar el DataFrame en un archivo CSV
df_predicciones.to_csv('predicciones_LSVR_34.csv', index=False)