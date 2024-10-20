from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS para permitir requisições de outros domínios
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

db_config = {
    'user': 'root',
    'password': 'root123',
    'host': '172.17.0.2',  # Endereço IP do contêiner do MySQL
    'port': '3306',
    'database': 'BaseDados_Projeto'
}

@app.route('/login', methods=['POST'])
def login():
    # Obtém os dados do usuário da requisição
    data = request.json

    # Verifica se os dados necessários foram fornecidos
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Conecta ao banco de dados
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            cursor = connection.cursor()
            # Executa uma consulta para verificar as credenciais do usuário
            cursor.execute("SELECT COUNT(*) FROM TUSERS WHERE USER_NOME = %s AND USER_PASS = %s", (username, password))
            user_count = cursor.fetchone()[0]  # Obtém o valor do primeiro elemento da tupla

            if user_count == 1:  # Verifica se o usuário existe
                return jsonify({"result": True}), 200
            else:
                return jsonify({"error": "Invalid username or password"}), 401

    except Error as e:
        return jsonify({"error": "Error connecting to the server: " + str(e)}), 500

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
