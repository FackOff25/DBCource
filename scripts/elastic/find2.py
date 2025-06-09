#! /bin/python3
import json
from elasticsearch import Elasticsearch
import pprint

# Параметры соединения с ES
client = Elasticsearch("http://localhost:9200")

# Индексы
rooms_id = "room"
clients_id = "clients"

searchBody = {
  "size": 0,
  "query": {
    "match": {
      "description": "люкс"
    }
  },
  "aggs": {
    "total_lux_rooms": {
      "value_count": {
        "field": "_id"
      }
    }
  }
}

result = client.search(index=rooms_id, body=searchBody)

result_str = json.dumps(result, indent=4, sort_keys=True)
with open("./2.json", "w+") as resultfile:
    resultfile.write(result_str)
pprint.pprint(result_str)
