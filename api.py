from flask import Flask, Response
from module_preprocess import pre_process

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
        df = pre_process()  # Suponemos que esta función devuelve un DataFrame
        json_result = df.to_json(orient='records')  # Convertir el DataFrame a JSON
        return Response(json_result, mimetype='application/json')  # Devolver el JSON como una respuesta HTTP
    except Exception as e:
        return Response(f"An error occurred: {str(e)}", status=500, mimetype='text/plain')

if __name__ == '__main__':  
    app.run(host= HOST, port=PORT, debug=True) 