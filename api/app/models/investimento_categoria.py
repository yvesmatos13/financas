from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class Investimento_categoria(BaseModel):
    _id: Optional[str]
    nome: str
    tipos: list  # Lista de tipos de investimentos nessa categoria

    class Config:
        json_encoders = {
            ObjectId: str
        }
