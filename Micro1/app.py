from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Para permitir requisições de qualquer origem (útil para o front-end em outra origem)

@app.route('/concat', methods=['POST'])
def concat_strings():
    data = request.json
    string1 = data.get('string1')
    string2 = data.get('string2')

    if not string1 or not string2:
        return jsonify({"error": "Both strings are required"}), 400

    concatenated = string1 + string2
    return jsonify({"result": concatenated}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
