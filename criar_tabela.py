import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect("wms.db")
cursor = conn.cursor()

# Cria a tabela 'leituras' se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS leituras (
        codigo TEXT PRIMARY KEY
    )
""")

conn.commit()
conn.close()
print("Tabela 'leituras' criada com sucesso.")