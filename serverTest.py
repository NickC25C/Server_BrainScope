import unittest
import pandas as pd
import numpy as np
from unidor import columns_to_csv
from generate_time import generate_time_column
from preprocesado import get_clean_data

class TestColumnsToCSV(unittest.TestCase):

    def test_columns_to_csv(self):
        # Definir algunos DataFrames de ejemplo
        time = pd.DataFrame({
            'time': [1, 2, 3]
        })

        engagement = pd.DataFrame({
            'engagement': [7, 8, 9]
        })

        memorization = pd.DataFrame({
            'memorization': [3, 4, 5]
        })

        workload = pd.DataFrame({
            'workload': [5, 6, 7]
        })

        # Llamar a la función
        result = columns_to_csv(time, engagement, memorization, workload)

        # Crear el DataFrame esperado
        expected_result = pd.DataFrame({
            'time': [1, 2, 3],
            'engagement': [7, 8, 9],
            'memorization': [3, 4, 5],
            'workload': [5, 6, 7]
        })

        # Verificar si el resultado es igual al esperado
        pd.testing.assert_frame_equal(result, expected_result)
    
    def test_generate_time_column(self):
        # Definir el tamaño de la columna que queremos generar
        length = 3

        # Llamar a la función con el tamaño deseado
        result = generate_time_column(length)

        # Crear el DataFrame esperado manualmente para comparar
        expected_times = [
            '0.000000',  # 00:00:00.000000
            '0.004000',  # 00:00:00.004000
            '0.008000'   # 00:00:00.008000
        ]
        expected_result = pd.DataFrame(expected_times, columns=['time(s)'])

        # Verificar si el resultado es igual al esperado
        pd.testing.assert_frame_equal(result, expected_result)

    def setUp(self):
        # Crear un DataFrame de datos simulados
        # 100 muestras, 12 canales (coincidiendo con ch_names en get_clean_data)
        self.data = pd.DataFrame(np.random.randn(100, 12), columns=[
            'AF7', 'Fp1', 'Fp2', 'AF8', 'F3', 'F4', 'P3', 'P4', 'PO7', 'O1', 'O2', 'PO8'
        ])

    def test_get_clean_data_memorization(self):
        # Probar la función con la métrica "Memorization"
        metric = "Memorization"
        result = get_clean_data(metric, self.data)

        # Verificar que el DataFrame de salida no esté vacío
        self.assertFalse(result.empty, "El DataFrame resultante no debería estar vacío.")

        # Verificar que las columnas de salida coinciden con la configuración esperada
        expected_columns = [
            'Alpha-P3', 'Alpha-P4', 'Alpha-F3', 'Alpha-F4',
            'Beta-P3', 'Beta-P4', 'Beta-F3', 'Beta-F4',
            'Theta-P3', 'Theta-P4', 'Theta-F3', 'Theta-F4',
            'Gamma-P3', 'Gamma-P4', 'Gamma-F3', 'Gamma-F4'
        ]
        for i in range(1, 9):
            for col in expected_columns:
                column_name = f'T{i}-{col}'
                self.assertIn(column_name, result.columns, f"Falta la columna {column_name} en el DataFrame resultante.")
    
    def test_get_clean_data_workload(self):
        # Probar la función con la métrica "Workload"
        metric = "Workload"
        result = get_clean_data(metric, self.data)

        # Verificar que el DataFrame de salida no esté vacío
        self.assertFalse(result.empty, "El DataFrame resultante no debería estar vacío.")

        # Verificar que las columnas de salida coinciden con la configuración esperada
        expected_columns = [
            'Alpha-P3', 'Alpha-P4',
            'Theta-P3', 'Theta-P4'
        ]
        for i in range(1, 9):
            for col in expected_columns:
                column_name = f'T{i}-{col}'
                self.assertIn(column_name, result.columns, f"Falta la columna {column_name} en el DataFrame resultante.")

    def test_get_clean_data_engagement(self):
        # Probar la función con la métrica "Engagement"
        metric = "Engagement"
        result = get_clean_data(metric, self.data)

        # Verificar que el DataFrame de salida no esté vacío
        self.assertFalse(result.empty, "El DataFrame resultante no debería estar vacío.")

        # Verificar que las columnas de salida coinciden con la configuración esperada
        expected_columns = [
            'Alpha-P3', 'Alpha-P4',
            'Beta-P3', 'Beta-P4',
            'Theta-P3', 'Theta-P4'
        ]
        for i in range(1, 9):
            for col in expected_columns:
                column_name = f'T{i}-{col}'
                self.assertIn(column_name, result.columns, f"Falta la columna {column_name} en el DataFrame resultante.")

    def test_filter_by_frequency(self):
        # Esta función podría ser testeada directamente también, asegurando que los datos son filtrados correctamente.
        pass

    def test_group_by_metric(self):
        # Probar la función group_by_metric con datos simulados
        pass


if __name__ == '__main__':
    unittest.main()