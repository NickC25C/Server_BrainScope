from flask import Flask, Response, request, jsonify
import pandas as pd
from module_preprocess import pre_process
import socket

import socket

def get_ip():
    local_hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
    filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
    return filtered_ips[:1][0]

HOST = get_ip()
PORT = "5000"

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        print("estamos aqui")
            # Asumir que los datos se envían como JSON en el cuerpo de la solicitud
        json_data = request.get_json()
        if not json_data:
            return Response("No JSON data provided", status=400, mimetype='text/plain')
        
        # Convertir los datos JSON a DataFrame
        df = pd.DataFrame(json_data)
        
        # Llamar a pre_process pasando el DataFrame
        processed_df = pre_process(df)

        json_result = processed_df.to_json(orient='records')  # Convertir el DataFrame a JSON
        return Response(json_result, mimetype='application/json')  # Devolver el JSON como una respuesta HTTP
    except Exception as e:
        return Response(f"An error occurred: {str(e)}", status=500, mimetype='text/plain')

if __name__ == '__main__':  
    app.run(host= HOST, port=PORT, debug=True) 