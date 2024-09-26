from motor.motor_asyncio import AsyncIOMotorClient

# Conectar ao MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')

# Nome do banco de dados
db = client['openfinance']
