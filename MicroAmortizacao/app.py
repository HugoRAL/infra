from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa a biblioteca CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

def calcular_juros_totais(divida, taxa_juros_anual, anos):
    # Convertendo taxa anual para mensal e anos para meses
    r = taxa_juros_anual / 100 / 12  # taxa de juros mensal em decimal
    n = anos * 12  # total de pagamentos em meses

    # Cálculo do pagamento mensal
    M = divida * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    # Cálculo do total pago e dos juros totais
    total_pago = M * n
    juros_totais = total_pago - divida

    return juros_totais

@app.route('/calcular_divida', methods=['POST'])
def calcular_divida():
    data = request.json
    
    # Obtendo os dados do JSON
    divida_total = data.get('divida_total')
    amortizacao = data.get('amortizacao')
    prestacao = data.get('prestacao')
    taxa_juros_anual = data.get('taxa_juros_anual')

    # Valida os dados recebidos
    if None in [divida_total, amortizacao, prestacao, taxa_juros_anual]:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    # Cálculo da dívida remanescente após a amortização
    divida_remanescente = divida_total - amortizacao

    # Calcular quantas prestações faltam para pagar a dívida
    meses = divida_remanescente / prestacao if prestacao > 0 else 0

    # Calcular os juros totais se a dívida for paga ao longo do tempo
    anos = meses / 12
    juros_totais = calcular_juros_totais(divida_remanescente, taxa_juros_anual, anos)

    return jsonify({
        "divida_remanescente": round(divida_remanescente, 2),
        "meses": round(meses, 2),
        "juros_totais": round(juros_totais, 2)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
