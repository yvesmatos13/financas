from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.receita import Receita, ReceitaResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from collections import OrderedDict
from typing import List

receita = APIRouter()

# Lista todas as receitas
@receita.get("/receitas", response_model=List[ReceitaResponse])
async def listar_receitas():
    receitas = await db['receitas'].find().to_list(1000)
    
    receitas_formatadas = []
    for receita in receitas:
        if '_id' in receita and isinstance(receita['_id'], ObjectId):
            receita['_id'] = str(receita['_id'])
        
        # Garantir que o campo "parcela" seja tratado corretamente
        recorrencia = receita.get('recorrencia', {"inicio": None, "fim": None, "intervalo": ""})
        
        # Criar uma versão formatada seguindo o modelo fornecido
        receita_formatada = {
            "id": receita["_id"],
            "descricao": receita.get("descricao", ""),
            "valor": receita.get("valor", 0.0),
            "data": receita.get("data", None),
            "categoria": receita.get("categoria", ""),
            "periodicidade": receita.get("periodicidade", ""),
            "tipo_pagamento": receita.get("tipo_pagamento", ""),
            "conta": receita.get("conta", ""),
            "observacao": receita.get("observacao", ""),
            "tipo_receita": receita.get("tipo_receita", ""),
            "recebido": receita.get("recebido", False),
            "recorrencia": receita.get('recorrencia', {"inicio": None, "fim": None, "intervalo": ""})
        }
        
        receitas_formatadas.append(receita_formatada)
    
    return jsonable_encoder(receitas_formatadas)

# Adiciona uma nova receita
@receita.post("/receitas/novo", response_model=ReceitaResponse)
async def criar_receita(receita_data: Receita):
    # Converter os dados da receita para um formato que possa ser armazenado no MongoDB
    receita_dict = receita_data.dict()
    
    # Inserir a nova receita no banco de dados
    nova_receita = await db['receitas'].insert_one(receita_dict)
    receita_id = nova_receita.inserted_id
    
    # Buscar a receita recém-criada para garantir que a resposta tenha o formato adequado
    receita = await db['receitas'].find_one({"_id": ObjectId(receita_id)})
    
    # Converter o _id para string e colocar em primeiro lugar
    if '_id' in receita and isinstance(receita['_id'], ObjectId):
        receita['_id'] = str(receita['_id'])
    
    # Retornar a receita no formato esperado
    return jsonable_encoder({
        "id": receita["_id"],
            "descricao": receita.get("descricao", ""),
            "valor": receita.get("valor", 0.0),
            "data": receita.get("data", None),
            "categoria": receita.get("categoria", ""),
            "periodicidade": receita.get("periodicidade", ""),
            "tipo_pagamento": receita.get("tipo_pagamento", ""),
            "conta": receita.get("conta", ""),
            "observacao": receita.get("observacao", ""),
            "tipo_receita": receita.get("tipo_receita", ""),
            "recebido": receita.get("recebido", False),
            "recorrencia": receita.get('recorrencia', {"inicio": None, "fim": None, "intervalo": ""})
    })

# Atualiza uma receita existente
@receita.put("/receitas/{id}", response_model=ReceitaResponse)
async def atualizar_receita(id: str, receita: Receita):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    receita_id = ObjectId(id)
    
    # Converta os dados de receita para um formato que pode ser atualizado no MongoDB
    receita_dict = receita.dict(exclude_unset=True)
    
    # Atualiza a receita no banco de dados
    resultado = await db['receitas'].update_one({"_id": receita_id}, {"$set": receita_dict})
    
    # Verifique se algum documento foi modificado
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    # Busque a receita atualizada
    receita = await db['receitas'].find_one({"_id": receita_id})
    
    # Verifique se a receita foi encontrada
    if receita is None:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    # Converta o _id para string
    if '_id' in receita and isinstance(receita['_id'], ObjectId):
        receita['_id'] = str(receita['_id'])
    
    # Retorne a receita atualizada
    return jsonable_encoder({
        "id": receita["_id"],
            "descricao": receita.get("descricao", ""),
            "valor": receita.get("valor", 0.0),
            "data": receita.get("data", None),
            "categoria": receita.get("categoria", ""),
            "periodicidade": receita.get("periodicidade", ""),
            "tipo_pagamento": receita.get("tipo_pagamento", ""),
            "conta": receita.get("conta", ""),
            "observacao": receita.get("observacao", ""),
            "tipo_receita": receita.get("tipo_receita", ""),
            "recebido": receita.get("recebido", False),
            "recorrencia": receita.get('recorrencia', {"inicio": None, "fim": None, "intervalo": ""})
    })

# Remove uma receita existente
@receita.delete("/receitas/{id}", status_code=204)
async def remover_receita(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    receita_id = ObjectId(id)
    
    # Tente remover a receita do banco de dados
    resultado = await db['receitas'].delete_one({"_id": receita_id})
    
    # Verifique se algum documento foi removido
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Receita não encontrada")

    # Retorna uma resposta vazia com status 204 (No Content)
    return None

# Busca uma receita por ID
@receita.get("/receitas/{id}", response_model=ReceitaResponse)
async def buscar_receita_por_id(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    receita_id = ObjectId(id)
    
    # Buscar a receita no banco de dados
    receita = await db['receitas'].find_one({"_id": receita_id})
    
    # Verifique se a receita foi encontrada
    if receita is None:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    # Converter o _id para string
    if '_id' in receita and isinstance(receita['_id'], ObjectId):
        receita['_id'] = str(receita['_id'])
    
    # Retornar a receita no formato esperado
    return jsonable_encoder({
        "id": receita["_id"],
            "descricao": receita.get("descricao", ""),
            "valor": receita.get("valor", 0.0),
            "data": receita.get("data", None),
            "categoria": receita.get("categoria", ""),
            "periodicidade": receita.get("periodicidade", ""),
            "tipo_pagamento": receita.get("tipo_pagamento", ""),
            "conta": receita.get("conta", ""),
            "observacao": receita.get("observacao", ""),
            "tipo_receita": receita.get("tipo_receita", ""),
            "recebido": receita.get("recebido", False),
            "recorrencia": receita.get('recorrencia', {"inicio": None, "fim": None, "intervalo": ""})
    })