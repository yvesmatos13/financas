from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.receita_categoria import Receita_categoria
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

receita_categoria = APIRouter()

# Lista todas as categorias
@receita_categoria.get("/receita_categorias")
async def listar_receita_categorias():
    receita_categorias = await db['receita_categorias'].find().to_list(1000)

    # Converter o _id para string
    for receita_categoria in receita_categorias:
        if '_id' in receita_categoria and isinstance(receita_categoria['_id'], ObjectId):
            receita_categoria['_id'] = str(receita_categoria['_id'])

    return jsonable_encoder(receita_categorias)
