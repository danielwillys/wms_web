import os
import sqlite3
from openpyxl import Workbook
from datetime import datetime

def exportar_relatorio_excel(turno=None, operador=None):
    # Cria a pasta 'relatorios' se não existir
    os.makedirs("relatorios", exist_ok=True)

    # Gera nome com data, turno e operador
    agora = datetime.now().strftime("%Y-%m-%d_%H-%M")
    partes_nome = ["relatorio"]

    if turno:
        partes_nome.append(f"turno{turno}")
    if operador:
        partes_nome.append(operador.replace(" ", "_"))

    partes_nome.append(agora)
    nome_arquivo = f"relatorios/{'_'.join(partes_nome)}.xlsx"

    # Conecta ao banco
    conn = sqlite3.connect("wms.db")
    cursor = conn.cursor()

    # Carrega pedidos
    cursor.execute("SELECT codigo, descricao FROM pedidos")
    pedidos = {codigo.strip().upper(): descricao for codigo, descricao in cursor.fetchall()}

    # Carrega leituras
    cursor.execute("SELECT codigo FROM leituras")
    leituras = [row[0].strip().upper() for row in cursor.fetchall()]

    # Classifica os códigos
    corretos = [c for c in leituras if c in pedidos]
    extras = [c for c in leituras if c not in pedidos]
    faltantes = [c for c in pedidos if c not in leituras]   

    # Cria planilha
    wb = Workbook()
    ws = wb.active
    ws.title = "Relatório WMS"

    # Cabeçalho
    ws.append(["Código", "Descrição", "Status"])

    # Preenche dados
    for codigo in corretos:
        ws.append([codigo, pedidos.get(codigo, ""), "Correto"])
    for codigo in extras:
        ws.append([codigo, "", "Extra"])
    for codigo in faltantes:
        ws.append([codigo, pedidos.get(codigo, ""), "Faltante"])

    # Salva arquivo
    wb.save(nome_arquivo)
    print(f"Relatório exportado para {nome_arquivo}")
    return nome_arquivo