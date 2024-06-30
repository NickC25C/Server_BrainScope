import pandas as pd
from datetime import datetime, timedelta

def generate_time_column(length):
    # Configuración inicial: hora de inicio y cantidad de marcas de tiempo a generar
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # Ajusta la hora de inicio sin microsegundos
    num_timestamps = length  # Por ejemplo, generar 1000 marcas de tiempo

    # Lista para almacenar las marcas de tiempo
    timestamps = []

    # Generar marcas de tiempo
    for i in range(num_timestamps):
        time_increment = start_time + timedelta(milliseconds=4 * i)
        timestamps.append(time_increment.strftime('%H:%M:%S.%f')[:-3])

    # Crear un DataFrame de pandas
    df = pd.DataFrame(timestamps, columns=['time(s)'])

    return df