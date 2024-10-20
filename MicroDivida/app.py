from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# URL do contêiner que já possui a função buscar_divida
BUSCAR_DIVIDA_URL = 'http://172.17.0.3:5000/buscar_divida'  # Atualizado para o novo IP

@app.route('/micro_buscar_divida', methods=['POST'])
def micro_buscar_divida():
    # Valida se o corpo da requisição é um JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json  
    user_id = data.get('user_id')  # Obtém o USER_ID do JSON

    # Verifica se o USER_ID foi fornecido e se é um número inteiro
    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    if not isinstance(user_id, int):
        return jsonify({"error": "User ID must be an integer"}), 400

    # Chama o contêiner existente
    response = requests.post(BUSCAR_DIVIDA_URL, json={"user_id": user_id})
    
    if response.status_code != 200:
        return jsonify(response.json()), response.status_code
    
    results = response.json()

    # Prepara os dados para a tabela
    table_data = []
    total_divida = 0
    taxa_juros = ""
    
    for record in results:
        divida_montante = record['DIVIDA_MONTANTE']
        divida_juros = record['DIVIDA_JURO']
        divida_pagamento_mensal = record['DIVIDA_PAGAMENTO_MENSAL']
        
        # Guarda a dívida total e a taxa de juros
        total_divida = divida_montante
        taxa_juros = f"{divida_juros}%"

        # Cria a linha da tabela para os próximos 5 meses
        for month in range(1, 6):
            # Calcula a dívida remanescente considerando as prestações pagas
            divida_restante = divida_montante - (divida_pagamento_mensal * (month - 1))

            # Garante que a dívida não seja negativa
            if divida_restante < 0:
                divida_restante = 0

            # Calcula a prestação mensal com juros
            prestacao = divida_pagamento_mensal + (divida_restante * (divida_juros / 100))

            # Define a data do pagamento (dia 1 de cada mês)
            data_vencimento = (datetime.now() + timedelta(days=30 * month)).replace(day=1)
            formatted_date = data_vencimento.strftime('%d/%m/%Y')

            # Adiciona o registro à tabela
            table_data.append({
                "divida_total": round(divida_restante, 2),  # Arredondar para 2 casas decimais
                "prestacao": round(prestacao, 2),           # Arredondar para 2 casas decimais
                "taxa_juros": f"{divida_juros}%",
                "data": formatted_date
            })

    # Retorna os dados
    return jsonify({
        "table_data": table_data,
        "total_divida": total_divida,
        "taxa_juros": taxa_juros
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)