from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Parcela(BaseModel):
    numero: int
    total: int

class Despesa(BaseModel):
    descricao: Optional[str]
    valor: float
    data: datetime
    categoria: str
    tipo_transacao: Optional[str]
    tipo_pagamento: Optional[str]
    conta: Optional[str]
    recorrente: bool
    parcela: Optional[Parcela]  # Submodelo para parcela
    observacoes: Optional[str]

    class Config:
        json_encoders = {
            ObjectId: str
        }

class DespesaResponse(BaseModel):
    id: Optional[str]
    descricao: Optional[str]
    valor: float
    data: datetime
    categoria: str
    tipo_transacao: Optional[str]
    tipo_pagamento: Optional[str]
    conta: Optional[str]
    recorrente: bool
    parcela: Optional[Parcela]  # Submodelo para parcela
    observacoes: Optional[str]

    class Config:
        from_attributes = True