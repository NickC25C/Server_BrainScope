from preprocesado import get_clean_data
from Workload.workload import process_workload
from Memorization.memorization import process_memorization
from Engagement.engagement import process_engagement
from generate_time import generate_time_column
from unidor import columns_to_csv
from io import BytesIO

def pre_process():

    data_preProcess = []
    data_process = []

    def get_max_iter():
        max_iter = len(data_process[0])
        for data in data_process:
            num_iter = len(data)
            if num_iter > max_iter: 
                max_iter = num_iter
        return max_iter


    # Cargar el archivo 27.csv en un objeto BytesIO
    with open("didi_eeg.csv", "rb") as file:
        contenido = file.read()
        archivo_objeto = BytesIO(contenido)
        archivo_objeto2 = BytesIO(contenido)
        archivo_objeto3 = BytesIO(contenido)

    data_preProcess.append(get_clean_data("Engagement", archivo_objeto3))
    data_preProcess.append(get_clean_data("Memorization", archivo_objeto2))
    data_preProcess.append(get_clean_data("Workload", archivo_objeto))

    data_process.append(process_engagement(data_preProcess[0]))
    data_process.append(process_memorization(data_preProcess[1]))
    data_process.append(process_workload(data_preProcess[2]))

    time_length = get_max_iter()
    column_time = generate_time_column(time_length)

    return columns_to_csv(column_time, data_process[0], data_process[1], data_process[2])


pre_process()



