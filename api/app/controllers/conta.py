from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.conta import Conta, ContaResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import List

conta = APIRouter()

# Lista todas as contas
@conta.get("/contas", response_model=List[ContaResponse])
async def listar_contas():
    contas = await db['contas'].find().to_list(1000)

    # Converter o _id para string
    contas_formatadas = []
    for conta in contas:
        if '_id' in conta and isinstance(conta['_id'], ObjectId):
            conta['_id'] = str(conta['_id'])

        conta_formatada = {
            "id": conta["_id"],
            "nome": conta.get("nome", ""),
            "descricao": conta.get("descricao", ""),
            "instituicao": conta.get("instituicao", ""),
            "numero_conta": conta.get("numero_conta", ""),
            "agencia": conta.get("agencia", ""),
            "saldo_inicial": conta.get("saldo_inicial", 0.0),
            "tipo_conta": conta.get("tipo_conta", ""),
            "moeda": conta.get("moeda", ""),
            "ativo": conta.get("ativo", False)
        }

        contas_formatadas.append(conta_formatada)

    return jsonable_encoder(contas_formatadas)

# Adiciona uma nova conta
@conta.post("/contas/novo", response_model=ContaResponse)
async def criar_conta(conta_data: Conta):
    # Converter os dados da conta para um formato que possa ser armazenado no MongoDB
    conta_dict = conta_data.dict()
    
    # Inserir a nova conta no banco de dados
    nova_conta = await db['contas'].insert_one(conta_dict)
    conta_id = nova_conta.inserted_id
    
    # Buscar a conta recém-criada para garantir que a resposta tenha o formato adequado
    conta_criada = await db['contas'].find_one({"_id": ObjectId(conta_id)})
    
    # Converter o _id para string e colocar em primeiro lugar
    if '_id' in conta_criada and isinstance(conta_criada['_id'], ObjectId):
        conta_criada['_id'] = str(conta_criada['_id'])
    
    # Retornar a conta no formato esperado
    return jsonable_encoder({
        "id": conta_criada["_id"],
            "nome": conta_criada.get("nome", ""),
            "descricao": conta_criada.get("descricao", ""),
            "instituicao": conta_criada.get("instituicao", ""),
            "numero_conta": conta_criada.get("numero_conta", ""),
            "agencia": conta_criada.get("agencia", ""),
            "saldo_inicial": conta_criada.get("saldo_inicial", 0.0),
            "tipo_conta": conta_criada.get("tipo_conta", ""),
            "moeda": conta_criada.get("moeda", ""),
            "ativo": conta_criada.get("ativo", False)
    })

# Atualiza uma conta existente
@conta.put("/contas/{id}", response_model=ContaResponse)
async def atualizar_conta(id: str, conta_atualizada: Conta):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    conta_id = ObjectId(id)
    
    # Converta os dados de conta para um formato que pode ser atualizado no MongoDB
    conta_dict = conta_atualizada.dict(exclude_unset=True)
    
    # Atualiza a conta no banco de dados
    resultado = await db['contas'].update_one({"_id": conta_id}, {"$set": conta_dict})
    
    # Verifique se algum documento foi modificado
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    # Busque a conta atualizada
    conta_atualizada = await db['contas'].find_one({"_id": conta_id})
    
    # Verifique se a conta foi encontrada
    if conta_atualizada is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    # Converta o _id para string
    if '_id' in conta_atualizada and isinstance(conta_atualizada['_id'], ObjectId):
        conta_atualizada['_id'] = str(conta_atualizada['_id'])
    
    # Retorne a conta atualizada
    return jsonable_encoder({
        "id": conta_atualizada["_id"],
        "descricao": conta_atualizada.get("descricao", ""),
        "valor": conta_atualizada.get("valor", 0.0),
        "data": conta_atualizada.get("data", ""),
        "categoria": conta_atualizada.get("categoria", ""),
        "tipo_transacao": conta_atualizada.get("tipo_transacao", ""),
        "tipo_pagamento": conta_atualizada.get("tipo_pagamento", ""),
        "conta": conta_atualizada.get("conta", ""),
        "recorrente": conta_atualizada.get("recorrente", False),
        "parcela": conta_atualizada.get("parcela", {"numero": 1, "total": 1}),
        "observacoes": conta_atualizada.get("observacoes", "")
    })

# Remove uma conta existente
@conta.delete("/contas/{id}", status_code=204)
async def remover_conta(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    conta_id = ObjectId(id)
    
    # Tente remover a conta do banco de dados
    resultado = await db['contas'].delete_one({"_id": conta_id})
    
    # Verifique se algum documento foi removido
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    # Retorna uma resposta vazia com status 204 (No Content)
    return None

# Busca uma conta por ID
@conta.get("/contas/{id}", response_model=ContaResponse)
async def buscar_conta_por_id(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    conta_id = ObjectId(id)
    
    # Buscar a conta no banco de dados
    conta_encontrada = await db['contas'].find_one({"_id": conta_id})
    
    # Verifique se a conta foi encontrada
    if conta_encontrada is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    # Converter o _id para string
    if '_id' in conta_encontrada and isinstance(conta_encontrada['_id'], ObjectId):
        conta_encontrada['_id'] = str(conta_encontrada['_id'])
    
    # Retornar a conta no formato esperado
    return jsonable_encoder({
        "id": conta_encontrada["_id"],
        "descricao": conta_encontrada.get("descricao", ""),
        "valor": conta_encontrada.get("valor", 0.0),
        "data": conta_encontrada.get("data", ""),
        "categoria": conta_encontrada.get("categoria", ""),
        "tipo_transacao": conta_encontrada.get("tipo_transacao", ""),
        "tipo_pagamento": conta_encontrada.get("tipo_pagamento", ""),
        "conta": conta_encontrada.get("conta", ""),
        "recorrente": conta_encontrada.get("recorrente", False),
        "parcela": conta_encontrada.get("parcela", {"numero": 1, "total": 1}),
        "observacoes": conta_encontrada.get("observacoes", "")
    })