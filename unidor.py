import pandas as pd

def columns_to_csv(time, engagement, memorization, workload):
    # Resetear los índices de cada DataFrame para asegurar que son únicos y están bien alineados
    time = time.reset_index(drop=True)
    engagement = engagement.reset_index(drop=True)
    memorization = memorization.reset_index(drop=True)
    workload = workload.reset_index(drop=True)

    # Crear un DataFrame con las columnas
    df_final = pd.concat([time, engagement, memorization, workload], axis=1)

    return df_final