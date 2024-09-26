from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.despesa import Despesa, DespesaResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from collections import OrderedDict
from typing import List

despesa = APIRouter()

# Lista todas as despesas
@despesa.get("/despesas", response_model=List[DespesaResponse])
async def listar_despesas():
    despesas = await db['despesas'].find().to_list(1000)
    
    despesas_formatadas = []
    for despesa in despesas:
        if '_id' in despesa and isinstance(despesa['_id'], ObjectId):
            despesa['_id'] = str(despesa['_id'])
        
        # Garantir que o campo "parcela" seja tratado corretamente
        parcela = despesa.get('parcela', {"numero": 1, "total": 1})
        
        # Criar uma versão formatada seguindo o modelo fornecido
        despesa_formatada = {
            "id": despesa["_id"],
            "descricao": despesa.get("descricao", ""),
            "valor": despesa.get("valor", 0.0),
            "data": despesa.get("data", ""),
            "categoria": despesa.get("categoria", ""),
            "tipo_transacao": despesa.get("tipo_transacao", ""),
            "tipo_pagamento": despesa.get("tipo_pagamento", ""),
            "conta": despesa.get("conta", ""),
            "recorrente": despesa.get("recorrente", False),
            "parcela": {
                "numero": parcela.get("numero", 1),
                "total": parcela.get("total", 1)
            },
            "observacoes": despesa.get("observacoes", "")
        }
        
        despesas_formatadas.append(despesa_formatada)
    
    return jsonable_encoder(despesas_formatadas)

# Adiciona uma nova despesa
@despesa.post("/despesas/novo", response_model=DespesaResponse)
async def criar_despesa(despesa_data: Despesa):
    # Converter os dados da despesa para um formato que possa ser armazenado no MongoDB
    despesa_dict = despesa_data.dict()
    
    # Inserir a nova despesa no banco de dados
    nova_despesa = await db['despesas'].insert_one(despesa_dict)
    despesa_id = nova_despesa.inserted_id
    
    # Buscar a despesa recém-criada para garantir que a resposta tenha o formato adequado
    despesa = await db['despesas'].find_one({"_id": ObjectId(despesa_id)})
    
    # Converter o _id para string e colocar em primeiro lugar
    if '_id' in despesa and isinstance(despesa['_id'], ObjectId):
        despesa['_id'] = str(despesa['_id'])
    
    # Retornar a despesa no formato esperado
    return jsonable_encoder({
        "id": despesa["_id"],
        "descricao": despesa.get("descricao", ""),
        "valor": despesa.get("valor", 0.0),
        "data": despesa.get("data", ""),
        "categoria": despesa.get("categoria", ""),
        "tipo_transacao": despesa.get("tipo_transacao", ""),
        "tipo_pagamento": despesa.get("tipo_pagamento", ""),
        "conta": despesa.get("conta", ""),
        "recorrente": despesa.get("recorrente", False),
        "parcela": despesa.get("parcela", {"numero": 1, "total": 1}),
        "observacoes": despesa.get("observacoes", "")
    })

# Atualiza uma despesa existente
@despesa.put("/despesas/{id}", response_model=DespesaResponse)
async def atualizar_despesa(id: str, despesa: Despesa):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    despesa_id = ObjectId(id)
    
    # Converta os dados de despesa para um formato que pode ser atualizado no MongoDB
    despesa_dict = despesa.dict(exclude_unset=True)
    
    # Atualiza a despesa no banco de dados
    resultado = await db['despesas'].update_one({"_id": despesa_id}, {"$set": despesa_dict})
    
    # Verifique se algum documento foi modificado
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    # Busque a despesa atualizada
    despesa = await db['despesas'].find_one({"_id": despesa_id})
    
    # Verifique se a despesa foi encontrada
    if despesa is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    # Converta o _id para string
    if '_id' in despesa and isinstance(despesa['_id'], ObjectId):
        despesa['_id'] = str(despesa['_id'])
    
    # Retorne a despesa atualizada
    return jsonable_encoder({
        "id": despesa["_id"],
        "descricao": despesa.get("descricao", ""),
        "valor": despesa.get("valor", 0.0),
        "data": despesa.get("data", ""),
        "categoria": despesa.get("categoria", ""),
        "tipo_transacao": despesa.get("tipo_transacao", ""),
        "tipo_pagamento": despesa.get("tipo_pagamento", ""),
        "conta": despesa.get("conta", ""),
        "recorrente": despesa.get("recorrente", False),
        "parcela": despesa.get("parcela", {"numero": 1, "total": 1}),
        "observacoes": despesa.get("observacoes", "")
    })

# Remove uma despesa existente
@despesa.delete("/despesas/{id}", status_code=204)
async def remover_despesa(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    despesa_id = ObjectId(id)
    
    # Tente remover a despesa do banco de dados
    resultado = await db['despesas'].delete_one({"_id": despesa_id})
    
    # Verifique se algum documento foi removido
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")

    # Retorna uma resposta vazia com status 204 (No Content)
    return None

# Busca uma despesa por ID
@despesa.get("/despesas/{id}", response_model=DespesaResponse)
async def buscar_despesa_por_id(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    despesa_id = ObjectId(id)
    
    # Buscar a despesa no banco de dados
    despesa = await db['despesas'].find_one({"_id": despesa_id})
    
    # Verifique se a despesa foi encontrada
    if despesa is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    # Converter o _id para string
    if '_id' in despesa and isinstance(despesa['_id'], ObjectId):
        despesa['_id'] = str(despesa['_id'])
    
    # Retornar a despesa no formato esperado
    return jsonable_encoder({
        "id": despesa["_id"],
        "descricao": despesa.get("descricao", ""),
        "valor": despesa.get("valor", 0.0),
        "data": despesa.get("data", ""),
        "categoria": despesa.get("categoria", ""),
        "tipo_transacao": despesa.get("tipo_transacao", ""),
        "tipo_pagamento": despesa.get("tipo_pagamento", ""),
        "conta": despesa.get("conta", ""),
        "recorrente": despesa.get("recorrente", False),
        "parcela": despesa.get("parcela", {"numero": 1, "total": 1}),
        "observacoes": despesa.get("observacoes", "")
    })