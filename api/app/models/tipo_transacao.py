from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Tipo_transacao(BaseModel):
    _id: Optional[str]
    nome: str
    descricao: str

    class Config:
        json_encoders = {
            ObjectId: str
        }
