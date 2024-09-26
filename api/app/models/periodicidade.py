from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Periodicidade(BaseModel):
    _id: Optional[str]
    nome: str  # Nome da periodicidade, ex: "Mensal", "Anual"
    descricao: Optional[str]  # Descrição opcional

    class Config:
        json_encoders = {
            ObjectId: str  # Converte ObjectId para string ao serializar
        }
