from preprocesado import get_clean_data
from Workload.workload import process_workload
from Memorization.memorization import process_memorization
from Engagement.engagement import process_engagement
from generate_time import generate_time_column
from unidor import columns_to_csv
from io import BytesIO

def pre_process(dataFrame):

    data_preProcess = []
    data_process = []

    def get_max_iter():
        max_iter = len(data_process[0])
        for data in data_process:
            num_iter = len(data)
            if num_iter > max_iter: 
                max_iter = num_iter
        return max_iter


    data_preProcess.append(get_clean_data("Engagement", dataFrame))
    data_preProcess.append(get_clean_data("Memorization", dataFrame))
    data_preProcess.append(get_clean_data("Workload", dataFrame))

    data_process.append(process_engagement(data_preProcess[0]))
    data_process.append(process_memorization(data_preProcess[1]))
    data_process.append(process_workload(data_preProcess[2]))

    time_length = get_max_iter()
    column_time = generate_time_column(time_length)

    return columns_to_csv(column_time, data_process[0], data_process[1], data_process[2])
