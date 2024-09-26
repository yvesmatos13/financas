from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.tipo_transacao import Tipo_transacao
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

tipo_transacao = APIRouter()

# Lista todas as categorias
@tipo_transacao.get("/tipo_transacaos")
async def listar_tipo_transacaos():
    tipo_transacaos = await db['tipo_transacaos'].find().to_list(1000)

    # Converter o _id para string
    for tipo_transacao in tipo_transacaos:
        if '_id' in tipo_transacao and isinstance(tipo_transacao['_id'], ObjectId):
            tipo_transacao['_id'] = str(tipo_transacao['_id'])

    return jsonable_encoder(tipo_transacaos)
