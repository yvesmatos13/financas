from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Conta(BaseModel):
    nome: str
    descricao: Optional[str] = None
    instituicao: str
    numero_conta: str
    agencia: str
    saldo_inicial: float
    tipo_conta_id: str
    moeda: str
    ativo: bool

    class Config:
        json_encoders = {
            ObjectId: str
        }

class ContaResponse(BaseModel):
    id: Optional[str]
    nome: str
    descricao: Optional[str] = None
    instituicao: str
    numero_conta: str
    agencia: str
    saldo_inicial: float
    tipo_conta: str
    moeda: str
    ativo: bool

    class Config:
        json_encoders = {
            ObjectId: str
        }