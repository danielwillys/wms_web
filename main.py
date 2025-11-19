import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import get_pedidos, conferir_item
from exportador import exportar_relatorio_excel

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
from jinja2 import StrictUndefined
templates = Jinja2Templates(
    directory="templates",
    auto_reload=True,
    undefined=StrictUndefined
)


# 🏠 Página principal com histórico e pedidos
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        pedidos = dict(get_pedidos())
        
        conn = sqlite3.connect("wms.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.codigo, p.descricao
            FROM leituras l
            LEFT JOIN pedidos p ON UPPER(TRIM(l.codigo)) = UPPER(TRIM(p.codigo))
            ORDER BY l.rowid DESC
            LIMIT 10
        """)
        historico = cursor.fetchall()
        conn.close()

        return templates.TemplateResponse("index.html", {
            "request": request,
            "historico": historico,
            "pedidos": pedidos
        })
    except Exception as e:
        logger.exception("Erro ao carregar a página principal")
        return HTMLResponse(content=f"<h1>Erro interno</h1><pre>{e}</pre>", status_code=500)

# 📥 Rota para registrar código escaneado
@app.post("/registrar_codigo")
async def registrar_codigo(codigo: str = Form(...)):
    codigo = codigo.strip().upper()
    conn = sqlite3.connect("wms.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO leituras (codigo) VALUES (?)", (codigo,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

# 📊 Rota do relatório visual
@app.get("/relatorio", response_class=HTMLResponse)
async def relatorio(request: Request):
    pedidos = dict(get_pedidos())

    conn = sqlite3.connect("wms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM leituras")
    leituras = [row[0].strip().upper() for row in cursor.fetchall()]
    conn.close()

    pedidos = {codigo.strip().upper(): descricao for codigo, descricao in pedidos.items()}

    corretos = [c for c in leituras if c in pedidos]
    extras = [c for c in leituras if c not in pedidos]
    faltantes = [c for c in pedidos if c not in leituras]

    return templates.TemplateResponse("relatorio.html", {
        "request": request,
        "corretos": corretos,
        "extras": extras,
        "faltantes": faltantes,
        "pedidos": pedidos
    })

# 📥 Rota para baixar o relatório Excel
@app.get("/baixar_excel")
async def baixar_excel(turno: str = "", operador: str = ""):
    nome_arquivo = exportar_relatorio_excel(turno=turno, operador=operador)
    return FileResponse(
        nome_arquivo,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=nome_arquivo
    )

# 🧹 Rota para limpar a tabela de leituras
@app.get("/limpar_leituras")
async def limpar_leituras():
    conn = sqlite3.connect("wms.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leituras")
    conn.commit()
    conn.close()
    print("Tabela 'leituras' limpa com sucesso.")
    return RedirectResponse(url="/", status_code=303)