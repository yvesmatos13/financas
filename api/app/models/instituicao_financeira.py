from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Instituicao_financeira(BaseModel):
    _id: Optional[str]
    nome: str
    tipo: str  # "Banco", "Banco Digital", etc.

    class Config:
        json_encoders = {
            ObjectId: str
        }
