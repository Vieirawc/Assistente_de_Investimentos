from flask import Flask, request, jsonify
from flask_cors import CORS
from db import usuarios_collection

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "API Assistente de Investimentos rodando!"})

#Classe ABC

# Criar usuário
@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    usuario = {
        "nome": data.get("nome"),
        "salario": float(data.get("salario", 0))
    }
    usuarios_collection.insert_one(usuario)
    return jsonify({"message": "Usuário cadastrado com sucesso!"})

# Listar usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = list(usuarios_collection.find({}, {"_id": 0}))
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
