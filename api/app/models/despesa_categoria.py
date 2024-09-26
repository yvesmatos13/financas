from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Despesa_categoria(BaseModel):
    _id: Optional[str]  # Defina _id como string, ou use ObjectId se preferir
    nome: str
    descricao: str

    class Config:
        json_encoders = {
            ObjectId: str  # Converte ObjectId para string ao serializar
        }
