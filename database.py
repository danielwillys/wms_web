import sqlite3

def get_pedidos():
    conn = sqlite3.connect("wms.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pedidos (codigo TEXT, descricao TEXT)")
    cursor.execute("SELECT codigo, descricao FROM pedidos")
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def conferir_item(codigo):
    conn = sqlite3.connect("wms.db")
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM pedidos WHERE codigo = ?", (codigo,))
    result = cursor.fetchone()
    conn.close()
    return "correto" if result else "extra"