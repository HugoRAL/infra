from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
CORS(app)

# Definindo métricas para o Prometheus
REQUEST_COUNT = Counter('divida_requests_total', 'Total number of requests to the /calcular_divida endpoint')
REQUEST_LATENCY = Histogram('divida_request_latency_seconds', 'Latency of /calcular_divida requests in seconds')

# Função para calcular juros totais
def calcular_juros_totais(divida, taxa_juros_anual, anos):
    r = taxa_juros_anual / 100 / 12
    n = anos * 12
    M = divida * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    total_pago = M * n
    juros_totais = total_pago - divida
    return juros_totais

@app.route('/calcular_divida', methods=['POST'])
def calcular_divida():
    REQUEST_COUNT.inc()  # Incrementando o contador de requisições

    # Medindo a latência da requisição
    with REQUEST_LATENCY.time():
        data = request.json
        divida_total = data.get('divida_total')
        amortizacao = data.get('amortizacao')
        prestacao = data.get('prestacao')
        taxa_juros_anual = data.get('taxa_juros_anual')

        if None in [divida_total, amortizacao, prestacao, taxa_juros_anual]:
            return jsonify({"error": "Todos os campos são obrigatórios."}), 400

        divida_remanescente = divida_total - amortizacao
        meses = divida_remanescente / prestacao if prestacao > 0 else 0
        anos = meses / 12
        juros_totais = calcular_juros_totais(divida_remanescente, taxa_juros_anual, anos)

        return jsonify({
            "divida_remanescente": round(divida_remanescente, 2),
            "meses": round(meses, 2),
            "juros_totais": round(juros_totais, 2)
        }), 200

# Rota para o Prometheus coletar métricas
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    # Usando o DispatcherMiddleware para integrar o /metrics com o aplicativo Flask
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    app.run(host='0.0.0.0', port=5003)
