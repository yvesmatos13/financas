from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.instituicao_financeira import Instituicao_financeira
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

instituicao_financeira = APIRouter()

# Lista todas as categorias
@instituicao_financeira.get("/instituicao_financeiras")
async def listar_instituicao_financeiras():
    instituicao_financeiras = await db['instituicao_financeiras'].find().to_list(1000)

    # Converter o _id para string
    for instituicao_financeira in instituicao_financeiras:
        if '_id' in instituicao_financeira and isinstance(instituicao_financeira['_id'], ObjectId):
            instituicao_financeira['_id'] = str(instituicao_financeira['_id'])

    return jsonable_encoder(instituicao_financeiras)
