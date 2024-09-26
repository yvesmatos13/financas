from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Tipo_conta(BaseModel):
    _id: Optional[str]
    nome: str
    descricao: Optional[str]

    class Config:
        json_encoders = {
            ObjectId: str
        }
