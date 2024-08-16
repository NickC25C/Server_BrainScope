import unittest
from flask import json
from api import app  # Asegúrate de que el archivo Flask se llame my_flask_app.py
from unittest.mock import patch
import pandas as pd
import numpy as np

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Configurar el cliente de prueba
        self.app = app.test_client()
        self.app.testing = True

    @patch('api.pre_process')
    def test_process_data_success(self, mock_pre_process):
        # Crear un DataFrame simulado para devolver como resultado de pre_process
        processed_data = pd.DataFrame({
            'time(s)': [0, 1, 2],
            'Engagement': [0.5, 0.6, 0.7],
            'Memorization': [0.4, 0.5, 0.6],
            'Workload': [0.3, 0.4, 0.5]
        })
        mock_pre_process.return_value = processed_data

        # Crear datos CSV simulados y convertirlos a un JSON string
        test_csv_data = "1,2,3\n4,5,6\n7,8,9\n"
        json_data = json.dumps(test_csv_data)

        # Realizar una solicitud POST a la ruta /process_data
        response = self.app.post('/process_data', data=json_data, content_type='application/json')

        # Verificar que la solicitud tuvo éxito (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Verificar que la respuesta es JSON y contiene los datos procesados
        response_data = json.loads(response.data)
        expected_response_data = processed_data.to_dict(orient='records')
        self.assertEqual(response_data, expected_response_data)

    def test_process_data_no_json(self):
        # Realizar una solicitud POST a la ruta /process_data sin datos JSON
        response = self.app.post('/process_data')

        # Verificar que la solicitud falla con el código de estado 500, dado el manejo actual
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'An error occurred:', response.data)

    @patch('api.pre_process')
    def test_process_data_error(self, mock_pre_process):
        # Configurar pre_process para que lance una excepción
        mock_pre_process.side_effect = Exception("Test error")

        # Crear datos CSV simulados y convertirlos a un JSON string
        test_csv_data = "1,2,3\n4,5,6\n7,8,9\n"
        json_data = json.dumps(test_csv_data)

        # Realizar una solicitud POST a la ruta /process_data
        response = self.app.post('/process_data', data=json_data, content_type='application/json')

        # Verificar que la solicitud falla con el código de estado 500
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'An error occurred: Test error', response.data)

if __name__ == '__main__':
    unittest.main()