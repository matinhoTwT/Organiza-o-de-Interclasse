import sqlite3

conn = sqlite3.connect("interclasse.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(times)")
colunas = cursor.fetchall()

for c in colunas:
    print(c)

conn.close()