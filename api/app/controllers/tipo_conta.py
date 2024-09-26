from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.tipo_conta import Tipo_conta
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

tipo_conta = APIRouter()

# Lista todas as categorias
@tipo_conta.get("/tipo_contas")
async def listar_tipo_contas():
    tipo_contas = await db['tipo_contas'].find().to_list(1000)

    # Converter o _id para string
    for tipo_conta in tipo_contas:
        if '_id' in tipo_conta and isinstance(tipo_conta['_id'], ObjectId):
            tipo_conta['_id'] = str(tipo_conta['_id'])

    return jsonable_encoder(tipo_contas)
