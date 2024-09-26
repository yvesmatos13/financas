from fastapi import FastAPI
from app.controllers.conta import conta
from app.controllers.despesa_categoria import despesa_categoria
from app.controllers.despesa import despesa
from app.controllers.instituicao_financeira import instituicao_financeira
from app.controllers.investimento_categoria import investimento_categoria
from app.controllers.investimento import investimento
from app.controllers.periodicidade import periodicidade
from app.controllers.receita_categoria import receita_categoria
from app.controllers.receita import receita
from app.controllers.tipo_conta import tipo_conta
from app.controllers.tipo_pagamento import tipo_pagamento
from app.controllers.tipo_receita import tipo_receita
from app.controllers.tipo_transacao import tipo_transacao

app = FastAPI()

prefix = "/api/v1"
# Registrar as rotas
app.include_router(conta, prefix=prefix)
app.include_router(despesa_categoria, prefix=prefix)
app.include_router(despesa, prefix=prefix)
app.include_router(instituicao_financeira, prefix=prefix)
app.include_router(investimento_categoria, prefix=prefix)
app.include_router(investimento, prefix=prefix)
app.include_router(periodicidade, prefix=prefix)
app.include_router(receita_categoria, prefix=prefix)
app.include_router(receita, prefix=prefix)
app.include_router(tipo_conta, prefix=prefix)
app.include_router(tipo_pagamento, prefix=prefix)
app.include_router(tipo_receita, prefix=prefix)
app.include_router(tipo_transacao, prefix=prefix)


# Iniciar o servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
