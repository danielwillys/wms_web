import sqlite3

conn = sqlite3.connect("wms.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS pedidos (codigo TEXT, descricao TEXT)")
cursor.execute("DELETE FROM pedidos")
cursor.executemany("INSERT INTO pedidos VALUES (?, ?)", [
    ("123456", "Produto A"),
    ("102030", "Produto B"),
    ("908070", "Produto C")
])
conn.commit()
conn.close()