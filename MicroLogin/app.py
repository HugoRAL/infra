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



@app.route('/buscar_divida', methods=['POST'])
def buscar_divida():
    # Valida se o corpo da requisição é um JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    # Obtém os dados do corpo da requisição
    data = request.json  
    user_id = data.get('user_id')  # Obtém o USER_ID do JSON

    # Verifica se o USER_ID foi fornecido e se é um número inteiro
    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400  # Retorna erro se USER_ID não for fornecido

    if not isinstance(user_id, int):
        return jsonify({"error": "User ID must be an integer"}), 400  # Retorna erro se USER_ID não for um inteiro

    try:
        # Conecta ao banco de dados
        connection = mysql.connector.connect(**db_config)

        # Verifica se a conexão foi bem-sucedida
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Usar dictionary=True para retornar resultados como dicionários
            
            # Executa a consulta para buscar as dívidas do usuário
            cursor.execute("""
                SELECT DIVIDA_MONTANTE, DIVIDA_JURO, DIVIDA_PAGAMENTO_MENSAL 
                FROM TDIVIDA 
                WHERE USER_ID = %s
            """, (user_id,))

            results = cursor.fetchall()  # Obtém todas as linhas do resultado

            if results:
                return jsonify(results), 200  # Retorna os resultados em formato JSON
            else:
                return jsonify({"error": "No debts found for this user ID"}), 404

    except Error as e:
        return jsonify({"error": "Error connecting to the server: " + str(e)}), 500

    finally:
        # Garante que o cursor e a conexão sejam fechados corretamente
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()



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
            cursor.execute("SELECT USER_ID FROM TUSERS WHERE USER_NOME = %s AND USER_PASS = %s", (username, password))
            result = cursor.fetchone()  # Obtém a primeira linha do resultado

            if result:  # Verifica se o usuário existe
                user_id = result[0]  # Obtém o USER_ID da tupla
                return jsonify({"result": True, "user_id": user_id}), 200
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
