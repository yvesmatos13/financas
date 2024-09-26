from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Transacao(BaseModel):
    tipo_transacao: str
    valor: float
    data: datetime

class DetalhesInvestimento(BaseModel):
    instituicao_financeira: str
    valor_investido: float
    data_aplicacao: datetime
    data_vencimento: datetime
    taxa_juros: float
    rentabilidade_atual: float

class Investimento(BaseModel):
    categoria: str
    tipo: str
    descricao: str
    detalhes: DetalhesInvestimento
    historico_transacoes: List[Transacao]
    tags: List[str]
    notas: Optional[str] = Field(default="")

class InvestimentoResponse(BaseModel):
    id: str
    categoria: str
    tipo: str
    descricao: str
    detalhes: DetalhesInvestimento
    historico_transacoes: List[Transacao]
    tags: List[str]
    notas: Optional[str] = Field(default="")