from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.periodicidade import Periodicidade
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

periodicidade = APIRouter()

# Lista todas as categorias
@periodicidade.get("/periodicidades")
async def listar_periodicidades():
    periodicidades = await db['periodicidades'].find().to_list(1000)

    # Converter o _id para string
    for periodicidade in periodicidades:
        if '_id' in periodicidade and isinstance(periodicidade['_id'], ObjectId):
            periodicidade['_id'] = str(periodicidade['_id'])

    return jsonable_encoder(periodicidades)
