import pandas as pd
from joblib import dump, load
from sklearn.svm import LinearSVR
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import max_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

def process_data_engagement():
    data = pd.read_csv('ProcessData.csv')
    data = data.dropna()

    #clf = joblib.load("Engagement_DTree_model_150.joblib")
    clf = joblib.load("Engagement_LSVR_model.joblib")

    predicciones = clf.predict(data)

    # Crear un DataFrame de pandas con las predicciones
    df_predicciones = pd.DataFrame(predicciones, columns=['Predicción'])

    # Guardar el DataFrame en un archivo CSV
    df_predicciones.to_csv('predicciones_34.csv', index=False)