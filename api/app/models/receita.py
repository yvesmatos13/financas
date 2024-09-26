from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Recorrencia(BaseModel):
    inicio: datetime
    fim: datetime
    intervalo: str

class Receita(BaseModel):
    descricao: str
    valor: float
    data: datetime
    categoria: str
    periodicidade: str
    tipo_pagamento: str
    conta: str
    observacao: Optional[str]
    tipo_receita: str
    recebido: bool
    recorrencia: Optional[Recorrencia]

    class Config:
        from_attributes = True  # Substitui orm_mode no Pydantic v2
        json_encoders = {ObjectId: str}

class ReceitaResponse(BaseModel):
    id: Optional[str]  # Converte o ObjectId para string
    descricao: str
    valor: float
    data: datetime
    categoria: str
    periodicidade: str
    tipo_pagamento: str
    conta: str
    observacao: Optional[str]
    tipo_receita: str
    recebido: bool
    recorrencia: Optional[Recorrencia]

    class Config:
        from_attributes = True  # Substitui orm_mode no Pydantic v2
        json_encoders = {ObjectId: str}

