import pandas as pd
import mne
from io import BytesIO
from autoreject import get_rejection_threshold
from scipy import signal
from mne.viz import plot_topomap
from mne import create_info
import matplotlib.pyplot as plt

metricas = ["Memorization", "Workload", "Engagement"]

frequencies_configuration = {
    "Valence": {
        "channels": ['AF7', 'AF8', 'Fp1', 'Fp2', 'F3', 'F4'],
        "frequencies": ["Alpha"],
    },
    "Memorization": {
        "channels": ['P3', 'P4', "F3", "F4"],
        "frequencies": ["Alpha", "Beta", "Theta", "Gamma"],
    },
    "Engagement": {
        "channels": ['P3', 'P4'],
        "frequencies": ["Alpha", "Beta", "Theta"],
    },
    "Workload":{
        "channels": ['P3', 'P4'],
        "frequencies": ["Alpha", "Theta"],
    }
}

def get_clean_data(metric, data):

    config = frequencies_configuration[metric]
    data = pd.read_csv(data)


    ch_names = ['AF7', 'Fp1', 'Fp2', 'AF8', 'F3', 'F4', 'P3', 'P4', 'PO7',
                'O1', 'O2', 'PO8']
    sfreq = 256  
    info = mne.create_info(ch_names, sfreq, ch_types='eeg')

    montage = mne.channels.make_standard_montage('standard_1020')
    info.set_montage(montage)

    #transpone los datos (columnas por filas)

    raw = mne.io.RawArray(data.transpose(), info)
    #raw.compute_psd().plot()

    ica_low_cut = 1.0       
    hi_cut  = 30
    raw_ica = raw.copy().filter(ica_low_cut, hi_cut)

    random_state = 42   # ensures ICA is reproducable each time it's run
    ica_n_components = .99     # Specify n_components as a decimal to set % explained variance


    ica = mne.preprocessing.ICA(n_components=ica_n_components,
                                random_state=random_state,
                                )

    ica.fit(raw_ica)


    ica_z_thresh = 1.96 
    eog_indices, eog_scores = ica.find_bads_eog(raw_ica, 
                                                ch_name=['Fp1', 'AF8'], 
                                                threshold=ica_z_thresh)
    ica.exclude = eog_indices


    info = create_info(ch_names, 1, "eeg")
    processed_data = ica.apply(raw_ica.copy())

    #---------------------------->aqui para los datos en crudo

    print("hola2")
    print(processed_data.get_data())
    #processed_data.compute_psd().plot()
    #plt.plot(np.zeros(shape=(3, 2)))
    plt.show(block=True)
    data_of_channels = processed_data.pick_channels(config["channels"]).get_data()

    bands = filter_by_frequency(processed_data, config["frequencies"])

    df = pd.DataFrame()

    for frequency in config["frequencies"]:
        band = bands[frequency]
        band_data = band.get_data()
        for i in range(len(config["channels"])):
            column_name = f'{frequency}-{config["channels"][i]}'
            df[column_name] = band_data[i]


    df.reset_index(drop=True, inplace=True)
    
    transformed_data = group_by_metric(df)
    transformed_data.to_csv(f'./{metric}/ProcessData.csv', index=False)
    return transformed_data

    # Filtramos los datos por bandas de frecuencia especificadas.
    
def filter_by_frequency(data, frequencies):

    iter_freqs = {
        'Theta': (4, 8),
        'Alpha': (8, 13),
        'Beta': (13, 22),
        'Gamma': (30, 45)
    }

    bands = {}
    for band in frequencies:
        low, hi = iter_freqs[band]
        bands[band] = data.copy().filter(low, hi)

    return bands


def group_by_metric(data):

    # recibimos un DataFrame como entrada y devolvemos 
    # una lista de nombres de columnas que se 
    # utilizarán para el DataFrame transformado.

    def columns_config(dt):
        columns = dt.columns.tolist()
        res = []
        for i in range(1,9):
            res.extend(list(map(lambda x: f"T{i}-{x}", columns)))
        return res

    # group_contigous_values se encarga de agrupar los datos 
    # según los valores de la columna "Valor", 
    # considerando solo los valores adyacentes que son iguales.

    def group_contiguous_values(data):
        # Crear una columna auxiliar que agrupa cada 8 filas
        data['group_identifier'] = (data.index // 8) + 1

        # Agrupar por el identificador de grupo
        grouped_data = data.groupby('group_identifier')
        return grouped_data

    def print_group_data(data):

        groups_of_9 = 0

        for group, group_data in grouped_data:
            group_id, valor = group
            length_of_group = len(list(group_data['Valor']))
            if(length_of_group != 8):
                groups_of_9 = groups_of_9 + 1
            print(f"Grupo {group_id}: {length_of_group}")
        print(groups_of_9)

    print(data.head(8))
    column_names = columns_config(data)
    #column_names.append("Valor")
    transformed_data = pd.DataFrame(columns=column_names)
    grouped_data = group_contiguous_values(data)
    #print_group_data(grouped_data)

    # eliminamos las columnas no deseadas del grupo actual y 
    # agregamos los valores de los datos al DataFrame transformed_data, 
    # junto con el valor de la métrica asociada.

    def callback(grp):
        # Eliminar la columna 'group_identifier'
        grp = grp.drop(['group_identifier'], axis=1)
        res = []
        for index, row in grp.iterrows():
            res.extend(row.tolist())
        # Antes de añadir a 'transformed_data', verifica si la longitud coincide
        if len(res) == len(transformed_data.columns):
            transformed_data.loc[len(transformed_data)] = res
        else:
            print(f"Error: intentando añadir {len(res)} elementos a DataFrame con {len(transformed_data.columns)} columnas.")
    
    grouped_data.apply(callback)
    return transformed_data



    
    

    
    
    
    



    


