from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.tipo_receita import Tipo_receita
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

tipo_receita = APIRouter()

# Lista todas as categorias
@tipo_receita.get("/tipo_receitas")
async def listar_tipo_receitas():
    tipo_receitas = await db['tipo_receitas'].find().to_list(1000)

    # Converter o _id para string
    for tipo_receita in tipo_receitas:
        if '_id' in tipo_receita and isinstance(tipo_receita['_id'], ObjectId):
            tipo_receita['_id'] = str(tipo_receita['_id'])

    return jsonable_encoder(tipo_receitas)
