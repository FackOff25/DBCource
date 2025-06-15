#! /bin/python3
from elasticsearch import Elasticsearch
import psycopg2
from sentence_transformers import SentenceTransformer

# подключение к ES для перекачки документов
es = Elasticsearch("http://localhost:9200")
# Модель для расчёта векторов
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# Длина вектора (если вдруг решим использовать другую модель)
embedding_dim = 384

# подключение к postgres, параметры как в ЛР
conn = psycopg2.connect(
	dbname="iu6",
	user="postgres",
	password="postgres",
	host="localhost",
	port="5432"
)
cur = conn.cursor()

# Запрос чтения всех записей из индекса ES
query = {
  "size": 1000,
  "query": {"match_all": {}}
}

# чтение документов из ES и запись результатов в переменные
response = es.search(index="clients", body=query)
clients_data = response["hits"]["hits"]

# Шаблон запроса создания таблицы клиентов с векторами
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
# Создание таблицы
cur.execute(comand)
conn.commit()

for client in clients_data:
  # расчёт вектора клиента
  embedding = model.encode(client["_source"]["card"]).tolist()

  # Запрос создания клиента
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
  # Примененте запроса создания клиента
  cur.execute(comand)
  conn.commit()

# Вывод для проверки результата
cur.execute('SELECT * FROM clients LIMIT 10')
for row in cur:
    print(row)