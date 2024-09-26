from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Receita_categoria(BaseModel):
    _id: Optional[str]
    nome: str
    descricao: str

    class Config:
        json_encoders = {
            ObjectId: str  # Converte ObjectId para string ao serializar
        }
