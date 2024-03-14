from pymongo import MongoClient

# Substitua pela sua string de conexão ao MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"
client = MongoClient(MONGO_DETAILS)

# Substitua 'meu_banco_de_dados' pelo nome do seu banco de dados
db = client.meu_banco_de_dados

# Função para inserir dados
def insert_data(collection, data):
    collection = db[collection]
    collection.insert_one(data)

# Função para buscar dados
def find_data(collection, query):
    collection = db[collection]
    data = collection.find_one(query)
    return data
