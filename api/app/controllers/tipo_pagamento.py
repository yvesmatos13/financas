from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.tipo_pagamento import Tipo_pagamento
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

tipo_pagamento = APIRouter()

# Lista todas as categorias
@tipo_pagamento.get("/tipo_pagamentos")
async def listar_tipo_pagamentos():
    tipo_pagamentos = await db['tipo_pagamentos'].find().to_list(1000)

    # Converter o _id para string
    for tipo_pagamento in tipo_pagamentos:
        if '_id' in tipo_pagamento and isinstance(tipo_pagamento['_id'], ObjectId):
            tipo_pagamento['_id'] = str(tipo_pagamento['_id'])

    return jsonable_encoder(tipo_pagamentos)
