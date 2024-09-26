from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.investimento_categoria import Investimento_categoria
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

investimento_categoria = APIRouter()

# Lista todas as categorias
@investimento_categoria.get("/investimento_categorias")
async def listar_investimento_categorias():
    investimento_categorias = await db['investimento_categorias'].find().to_list(1000)

    # Converter o _id para string
    for investimento_categoria in investimento_categorias:
        if '_id' in investimento_categoria and isinstance(investimento_categoria['_id'], ObjectId):
            investimento_categoria['_id'] = str(investimento_categoria['_id'])

    return jsonable_encoder(investimento_categorias)
