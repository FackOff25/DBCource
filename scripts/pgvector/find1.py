#! /bin/python3
import psycopg2

# подключение к postgres, параметры как в ЛР
conn = psycopg2.connect(
	dbname="iu6",
	user="postgres",
	password="postgres",
	host="localhost",
	port="5432"
)
cur = conn.cursor()

id_to_search = 1

comand = f""" 
SELECT card,
    embedding <-> (SELECT embedding FROM clients WHERE id = {id_to_search}) as distance
FROM clients 
WHERE id != {id_to_search} 
ORDER BY distance
LIMIT 5;
"""
cur.execute(comand)
for row in cur:
    print(row)

