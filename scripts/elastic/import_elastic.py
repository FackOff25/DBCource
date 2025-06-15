#! /bin/python3
import json
from elasticsearch import Elasticsearch

# Параметры соединения с ES
client = Elasticsearch("http://localhost:9200")

# Документы
rooms = "/inputs/rooms.json"
clients = "/inputs/clients.json"

# Названия индексов
rooms_id = "room"
clients_id = "clients"

# Анализатор
analyzer_settings = {
  "settings": {
    "analysis": {
      "analyzer": {
        "russian_analyzer": { # идентификатор анализатора
          "tokenizer": "standard", # убирает пунктуацию и делит текст на слова
          "filter": [
            "lowercase", # переводит в нижний регистр
            "russian_stop", # удаляет "стоп слова"
            "russian_snowball" # удаляет всё, кроме основы слов
            ]
        }
      },
      "filter": {
        "russian_stop": {
          "type": "stop",
          "stopwords": "_russian_"
        },
        "russian_snowball": {
          "type": "snowball",
          "language": "Russian"
        }
      }
    }
  }
}

# маппинги
mapping_rooms = { 
    "mappings": {
     "properties": {
      "index": {"type": "keyword"},
      "doc_type":{"type": "keyword"},
      "id": {"type": "integer"},
      "description": {"type": "text", "analyzer": "russian_analyzer"}, # применяем анализатор
      "day_price": {"type": "integer"},
    }
  }
}
  
mapping_clients = {
  "mappings": {
    "properties": {
      "index":{"type": "keyword"},
      "doc_type": {"type": "keyword"},
      "id":{"type": "integer"},
      "client_id": {"type": "keyword"},
      "card": {"type": "text", "analyzer": "russian_analyzer"},
      "arriving_date": {"type": "date"},
      "staying_period": {"type": "integer"},
      "services": {"type": "text", "analyzer": "russian_analyzer"},
      "room_id": {"type": "keyword"},
    }
  }
}


print("Creating an index...")

# Удаление потенциально существующих индексов
if client.indices.exists(index=rooms_id):
  print("Recreate " + rooms_id + " index")
  client.indices.delete(index=rooms_id)
  client.indices.create(index=rooms_id, body={**analyzer_settings, **mapping_rooms})
else:
  print("Create " + rooms_id)
  client.indices.create(index=rooms_id, body={**analyzer_settings, **mapping_rooms})

if client.indices.exists(index=clients_id):
  print("Recreate " + clients_id + " index")
  client.indices.delete(index=clients_id)
  client.indices.create(index=clients_id, body={**analyzer_settings, **mapping_clients})
else:
  print("Create " + clients_id)
  client.indices.create(index=clients_id, body={**analyzer_settings, **mapping_clients})

print("Importing documents...")
with open(rooms, 'r') as file_data:
  #чтение комнат из файла
  dataStore = json.load(file_data)
for data in dataStore:
  try:
    # запись комнат в БД
    client.index(index=data["index"],
      id=data["id"],
      body=data["body"]
      )
  except Exception as e:
    print(e)
    exit(1)
print('Document ' + rooms + ' has been read')

with open(clients, 'r') as file_data:
  #чтение клиентов из файла
	dataStore = json.load(file_data)
for data in dataStore:
  try:
     # запись клиентов в БД
    client.index(index=data["index"],
        id=data["id"],
        body=data["body"]
        )
  except Exception as e:
    print(e)
    exit(1)
print('Document ' + clients + ' has been read')


print("All documents indexed successfully")
