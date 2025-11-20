from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/assistente_investimentos')
client = MongoClient(mongo_uri)
db = client.get_database()

# --- ROTAS DE EMPRESAS ---
@app.route('/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'POST':
        data = request.json
        data['rendimento'] = float(data.get('rendimento', 0))
        res = db.investimentos.insert_one(data)
        return jsonify({"id": str(res.inserted_id), "msg": "Criado"}), 201
    
    projects = []
    for doc in db.investimentos.find():
        doc['id'] = str(doc['_id'])
        del doc['_id']
        projects.append(doc)
    return jsonify(projects)

@app.route('/projects/<id>', methods=['GET', 'DELETE', 'PUT'])
def handle_project_id(id):
    if request.method == 'GET':
        doc = db.investimentos.find_one({"_id": ObjectId(id)})
        if doc:
            doc['id'] = str(doc['_id'])
            del doc['_id']
            return jsonify(doc)
        return jsonify({"error": "Não encontrado"}), 404
    if request.method == 'DELETE':
        db.investimentos.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Deletado"})
    if request.method == 'PUT':
        data = request.json
        db.investimentos.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"msg": "Atualizado"})

# --- ROTAS DE CLIENTES ---
@app.route('/clients', methods=['GET', 'POST'])
def handle_clients():
    if request.method == 'POST':
        data = request.json
        res = db.clientes.insert_one(data)
        return jsonify({"id": str(res.inserted_id), "msg": "Cliente cadastrado"}), 201
    
    clients = []
    for doc in db.clientes.find():
        doc['id'] = str(doc['_id'])
        del doc['_id']
        clients.append(doc)
    return jsonify(clients)

@app.route('/clients/<id>', methods=['DELETE', 'PUT'])
def handle_client_id(id):
    if request.method == 'DELETE':
        db.clientes.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Cliente removido"})
    if request.method == 'PUT':
        data = request.json
        db.clientes.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"msg": "Cliente atualizado"})

# --- ROTAS DE CARTEIRA ---
@app.route('/portfolio', methods=['POST'])
def save_portfolio():
    data = request.json
    # O MongoDB aceita campos novos automaticamente, então o 'aporte_mensal' será salvo aqui
    res = db.carteira.insert_one(data)
    return jsonify({"id": str(res.inserted_id), "msg": "Investimento registrado"}), 201

@app.route('/portfolio/<id>', methods=['DELETE', 'PUT'])
def handle_portfolio_item(id):
    if request.method == 'DELETE':
        db.carteira.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Investimento resgatado/removido"})
    
    if request.method == 'PUT':
        data = request.json
        db.carteira.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"msg": "Investimento atualizado"})

@app.route('/portfolio/client/<client_id>', methods=['GET'])
def get_client_stats(client_id):
    items = list(db.carteira.find({"cliente_id": client_id}))
    
    portfolio_detalhado = []
    stats = { 'total_investido': 0.0, 'renda_mensal_projetada': 0.0, 'renda_anual_projetada': 0.0 }
    distribuicao = {'Acao': 0, 'FII': 0, 'Renda_Fixa': 0, 'Outro': 0}

    for item in items:
        empresa = db.investimentos.find_one({"_id": ObjectId(item['empresa_id'])})
        
        if empresa:
            valor_inv = float(item.get('valor_inicial', 0))
            aporte_mensal = float(item.get('aporte_mensal', 0)) # Novo Campo
            
            taxa_ano = float(empresa.get('rendimento', 0))
            tipo = empresa.get('tipo_investimento', 'Outro')

            # Cálculo simples de rendimento sobre o valor JÁ investido (Patrimônio Atual)
            lucro_ano = valor_inv * (taxa_ano / 100)
            lucro_mes = lucro_ano / 12

            stats['total_investido'] += valor_inv
            stats['renda_anual_projetada'] += lucro_ano
            stats['renda_mensal_projetada'] += lucro_mes
            
            if tipo in distribuicao: distribuicao[tipo] += valor_inv
            else: distribuicao['Outro'] += valor_inv

            portfolio_detalhado.append({
                "id": str(item['_id']),
                "empresa": empresa.get('nome'),
                "tipo": tipo,
                "valor_aplicado": valor_inv,
                "aporte_mensal": aporte_mensal, # Enviando para o frontend
                "taxa": taxa_ano,
                "meta": item.get('meta'),
                "renda_mensal": lucro_mes
            })

    return jsonify({ "lista": portfolio_detalhado, "totais": stats, "grafico": distribuicao })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)