import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from module_preprocess import pre_process  # Ajusta según el nombre del archivo que contiene tu función.

class TestPreProcess(unittest.TestCase):

    @patch('module_preprocess.get_clean_data')
    @patch('module_preprocess.process_engagement')
    @patch('module_preprocess.process_memorization')
    @patch('module_preprocess.process_workload')
    @patch('module_preprocess.generate_time_column')
    @patch('module_preprocess.columns_to_csv')
    def test_pre_process(self, mock_columns_to_csv, mock_generate_time_column, mock_process_workload, 
                         mock_process_memorization, mock_process_engagement, mock_get_clean_data):
        # Configurar las funciones mock para devolver valores simulados
        mock_get_clean_data.side_effect = [
            pd.DataFrame(np.random.randn(10, 5)),  # Simulación para Engagement
            pd.DataFrame(np.random.randn(10, 5)),  # Simulación para Memorization
            pd.DataFrame(np.random.randn(10, 5))   # Simulación para Workload
        ]

        mock_process_engagement.return_value = pd.DataFrame(np.random.randn(8, 5))
        mock_process_memorization.return_value = pd.DataFrame(np.random.randn(9, 5))
        mock_process_workload.return_value = pd.DataFrame(np.random.randn(7, 5))

        mock_generate_time_column.return_value = pd.DataFrame({'time(s)': np.linspace(0, 7, 8)})

        mock_columns_to_csv.return_value = pd.DataFrame({
            'time(s)': np.linspace(0, 7, 8),
            'Engagement': np.random.randn(8),
            'Memorization': np.random.randn(8),
            'Workload': np.random.randn(8)
        })

        # Crear un DataFrame de entrada simulado
        dataFrame = pd.DataFrame(np.random.randn(100, 12))

        # Llamar a la función que estamos probando
        result = pre_process(dataFrame)

        # Verificar que las funciones externas se llamaron con los argumentos correctos
        mock_get_clean_data.assert_any_call("Engagement", dataFrame)
        mock_get_clean_data.assert_any_call("Memorization", dataFrame)
        mock_get_clean_data.assert_any_call("Workload", dataFrame)

        # Verificar que la función generate_time_column se llamó con el valor correcto
        mock_generate_time_column.assert_called_once_with(9)  # max_iter debería ser 9 aquí

        # Verificar que columns_to_csv se llamó una vez
        mock_columns_to_csv.assert_called_once()

        # Verificar que el resultado no esté vacío y tenga la estructura esperada
        self.assertFalse(result.empty, "El DataFrame resultante no debería estar vacío.")
        expected_columns = ['time(s)', 'Engagement', 'Memorization', 'Workload']
        self.assertListEqual(result.columns.tolist(), expected_columns, "Las columnas del DataFrame no coinciden con las esperadas.")

if __name__ == '__main__':
    unittest.main()