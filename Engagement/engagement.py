import pandas as pd
import joblib

#def process_data_engagement():
data = pd.read_csv('ProcessData.csv')
data = data.dropna()

#clf = joblib.load("Engagement_DTree_model_150.joblib")
clf = joblib.load("Engagement_LSVR_model.joblib")

predicciones = clf.predict(data)

# Crear un DataFrame de pandas con las predicciones
df_predicciones = pd.DataFrame(predicciones, columns=['Predicción'])

# Guardar el DataFrame en un archivo CSV
df_predicciones.to_csv('predicciones_34.csv', index=False)