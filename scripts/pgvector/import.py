#! /bin/python3
from elasticsearch import Elasticsearch
import psycopg2
from sentence_transformers import SentenceTransformer

#the index client used to communicate with the database
es = Elasticsearch("http://localhost:9200")
# Модель для
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embedding_dim = 384

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

response = es.search(index="clients", body=query)
clients_data = response["hits"]["hits"]
services = [
  "breakfast",
  "cleaning",
  "dinner",
  "gym",
  "spa"
]

comand = """
CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY,
    card TEXT NOT NULL,
    arriving_date DATE NOT NULL,
    staying_period INT NOT NULL,
    room_id INT NOT NULL,
    services TEXT NOT NULL,
    embedding VECTOR("""+str(384)+""") NOT NULL
);
"""
cur.execute(comand)
conn.commit()

for client in clients_data:
  client_sevices = client["_source"]["services"]
  embedding = model.encode(client["_source"]["card"]).tolist()

  comand = f"""
    INSERT INTO clients (card, arriving_date, staying_period, room_id, services, embedding)
    VALUES (
        '{client["_source"]["card"]}',
        '{client["_source"]["arriving_date"]}',
        {int(client["_source"]["staying_period"])},
        {int(client["_source"]["room_id"])},
        '{" ".join(str(s) for s in client["_source"]["services"])}',
        '{embedding}'::vector
    );
  """

  cur.execute(comand)
  conn.commit()

cur.execute('SELECT * FROM clients LIMIT 10')
for row in cur:
    print(row)