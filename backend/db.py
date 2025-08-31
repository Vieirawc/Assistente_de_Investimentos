from pymongo import MongoClient

# Conexão com o MongoDB
client = MongoClient("mongodb://host.docker.internal:27017/")
db = client["assistente_investimentos"]

# Coleção de usuários
usuarios_collection = db["usuarios"]