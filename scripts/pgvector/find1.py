#! /bin/python3
import psycopg2

#the index client used to communicate with the database

conn = psycopg2.connect(
	dbname="iu6",
	user="postgres",
	password="postgres",
	host="localhost",
	port="5432"
)
cur = conn.cursor()

query = {
  "size": 1000,
  "query": {"match_all": {}}
}

id_to_search = 1

comand = f""" 
SELECT *,
    embedding <-> (SELECT embedding FROM clients WHERE id = {id_to_search}) as distance
FROM clients 
WHERE id != {id_to_search} 
ORDER BY distance
LIMIT 5;
"""
cur.execute(comand)
for row in cur:
    print(row)

