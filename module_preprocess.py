from preprocesado import get_clean_data
from io import BytesIO

metricas = ["Memorization", "Workload", "Engagement"]

# Cargar el archivo 27.csv en un objeto BytesIO
with open("didi_eeg.csv", "rb") as file:
    contenido = file.read()
    archivo_objeto = BytesIO(contenido)
    archivo_objeto2 = BytesIO(contenido)
    archivo_objeto3 = BytesIO(contenido)

get_clean_data("Workload", archivo_objeto)
get_clean_data("Memorization", archivo_objeto2)
get_clean_data("Engagement", archivo_objeto3)
