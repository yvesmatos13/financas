from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.despesa_categoria import Despesa_categoria
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

despesa_categoria = APIRouter()

# Lista todas as categorias para despesas
@despesa_categoria.get("/despesa_categorias")
async def listar_despesa_categorias():
    despesa_categorias = await db['despesa_categorias'].find().to_list(1000)

    # Converter o _id para string
    for despesa_categoria in despesa_categorias:
        if '_id' in despesa_categoria and isinstance(despesa_categoria['_id'], ObjectId):
            despesa_categoria['_id'] = str(despesa_categoria['_id'])

    return jsonable_encoder(despesa_categorias)
