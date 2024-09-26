from fastapi import APIRouter, HTTPException
from app.db_config.database import db
from app.models.investimento import Investimento, InvestimentoResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from collections import OrderedDict
from typing import List

investimento = APIRouter()

# Lista todas as investimentos
@investimento.get("/investimentos", response_model=List[InvestimentoResponse])
async def listar_investimentos():
    investimentos = await db['investimentos'].find().to_list(1000)
    
    investimentos_formatadas = []
    for investimento in investimentos:
        if '_id' in investimento and isinstance(investimento['_id'], ObjectId):
            investimento['_id'] = str(investimento['_id'])
        
        # Garantir que o campo "parcela" seja tratado corretamente
        recorrencia = investimento.get('recorrencia', {"inicio": None, "fim": None, "intervalo": ""})
        
        # Criar uma versão formatada seguindo o modelo fornecido
        investimento_formatada = {
            "id": investimento["_id"],
            "categoria": investimento.get("categoria", ""),
            "tipo": investimento.get("tipo", ""),
            "descricao": investimento.get("descricao", ""),
            "detalhes": investimento.get("detalhes", 
                                                    {
                                                        "instituicao_financeira": "",
                                                        "valor_investido": 0.0,
                                                        "data_aplicacao": None,
                                                        "data_vencimento": None,
                                                        "taxa_juros": 0.0,
                                                        "rentabilidade_atual": 0.0
                                                    }),
            "historico_transacoes": investimento.get("historico_transacoes", [
                {"tipo_transacao":"",
                 "valor": 0.0,
                 "data": None
                 }
            ]),
            "tags": investimento.get("tags", []),
            "notas": investimento.get("notas", "")
        }
        
        investimentos_formatadas.append(investimento_formatada)
    
    return jsonable_encoder(investimentos_formatadas)

# Adiciona uma nova investimento
@investimento.post("/investimentos/novo", response_model=InvestimentoResponse)
async def criar_investimento(investimento_data: Investimento):
    # Converter os dados da investimento para um formato que possa ser armazenado no MongoDB
    investimento_dict = investimento_data.dict()
    
    # Inserir a nova investimento no banco de dados
    nova_investimento = await db['investimentos'].insert_one(investimento_dict)
    investimento_id = nova_investimento.inserted_id
    
    # Buscar a investimento recém-criada para garantir que a resposta tenha o formato adequado
    investimento = await db['investimentos'].find_one({"_id": ObjectId(investimento_id)})
    
    # Converter o _id para string e colocar em primeiro lugar
    if '_id' in investimento and isinstance(investimento['_id'], ObjectId):
        investimento['_id'] = str(investimento['_id'])
    
    # Retornar a investimento no formato esperado
    return jsonable_encoder({
        "id": investimento["_id"],
            "categoria": investimento.get("categoria", ""),
            "tipo": investimento.get("tipo", ""),
            "descricao": investimento.get("descricao", ""),
            "detalhes": investimento.get("detalhes", 
                                                    {
                                                        "instituicao_financeira": "",
                                                        "valor_investido": 0.0,
                                                        "data_aplicacao": None,
                                                        "data_vencimento": None,
                                                        "taxa_juros": 0.0,
                                                        "rentabilidade_atual": 0.0
                                                    }),
            "historico_transacoes": investimento.get("historico_transacoes", [
                {"tipo_transacao":"",
                 "valor": 0.0,
                 "data": None
                 }
            ]),
            "tags": investimento.get("tags", []),
            "notas": investimento.get("notas", "")
    })

# Atualiza uma investimento existente
@investimento.put("/investimentos/{id}", response_model=InvestimentoResponse)
async def atualizar_investimento(id: str, investimento: Investimento):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    investimento_id = ObjectId(id)
    
    # Converta os dados de investimento para um formato que pode ser atualizado no MongoDB
    investimento_dict = investimento.dict(exclude_unset=True)
    
    # Atualiza a investimento no banco de dados
    resultado = await db['investimentos'].update_one({"_id": investimento_id}, {"$set": investimento_dict})
    
    # Verifique se algum documento foi modificado
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Investimento não encontrada")
    
    # Busque a investimento atualizada
    investimento = await db['investimentos'].find_one({"_id": investimento_id})
    
    # Verifique se a investimento foi encontrada
    if investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrada")
    
    # Converta o _id para string
    if '_id' in investimento and isinstance(investimento['_id'], ObjectId):
        investimento['_id'] = str(investimento['_id'])
    
    # Retorne a investimento atualizada
    return jsonable_encoder({
        "id": investimento["_id"],
            "categoria": investimento.get("categoria", ""),
            "tipo": investimento.get("tipo", ""),
            "descricao": investimento.get("descricao", ""),
            "detalhes": investimento.get("detalhes", 
                                                    {
                                                        "instituicao_financeira": "",
                                                        "valor_investido": 0.0,
                                                        "data_aplicacao": None,
                                                        "data_vencimento": None,
                                                        "taxa_juros": 0.0,
                                                        "rentabilidade_atual": 0.0
                                                    }),
            "historico_transacoes": investimento.get("historico_transacoes", [
                {"tipo_transacao":"",
                 "valor": 0.0,
                 "data": None
                 }
            ]),
            "tags": investimento.get("tags", []),
            "notas": investimento.get("notas", "")
    })

# Remove uma investimento existente
@investimento.delete("/investimentos/{id}", status_code=204)
async def remover_investimento(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    investimento_id = ObjectId(id)
    
    # Tente remover a investimento do banco de dados
    resultado = await db['investimentos'].delete_one({"_id": investimento_id})
    
    # Verifique se algum documento foi removido
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Investimento não encontrada")

    # Retorna uma resposta vazia com status 204 (No Content)
    return None

# Busca uma investimento por ID
@investimento.get("/investimentos/{id}", response_model=InvestimentoResponse)
async def buscar_investimento_por_id(id: str):
    # Verificar se o id é um ObjectId válido
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converta o id para ObjectId
    investimento_id = ObjectId(id)
    
    # Buscar a investimento no banco de dados
    investimento = await db['investimentos'].find_one({"_id": investimento_id})
    
    # Verifique se a investimento foi encontrada
    if investimento is None:
        raise HTTPException(status_code=404, detail="Investimento não encontrada")
    
    # Converter o _id para string
    if '_id' in investimento and isinstance(investimento['_id'], ObjectId):
        investimento['_id'] = str(investimento['_id'])
    
    # Retornar a investimento no formato esperado
    return jsonable_encoder({
        "id": investimento["_id"],
            "categoria": investimento.get("categoria", ""),
            "tipo": investimento.get("tipo", ""),
            "descricao": investimento.get("descricao", ""),
            "detalhes": investimento.get("detalhes", 
                                                    {
                                                        "instituicao_financeira": "",
                                                        "valor_investido": 0.0,
                                                        "data_aplicacao": None,
                                                        "data_vencimento": None,
                                                        "taxa_juros": 0.0,
                                                        "rentabilidade_atual": 0.0
                                                    }),
            "historico_transacoes": investimento.get("historico_transacoes", [
                {"tipo_transacao":"",
                 "valor": 0.0,
                 "data": None
                 }
            ]),
            "tags": investimento.get("tags", []),
            "notas": investimento.get("notas", "")
    })