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
  "aggs": {
    "arrival_by_year": {
      "date_histogram": {
        "field": "arriving_date",
        "calendar_interval": "1y",
      },
      "aggs": {
        "rooms_aggregation": {
          "terms": {
            "field": "room_id",
            "size": 10
          }
        }
      }
    }
  }
}

result = client.search(index=clients_id, body=searchBody)

result_str = json.dumps(result, indent=4, sort_keys=True)
with open("./1.json", "w+") as resultfile:
    resultfile.write(result_str)
pprint.pprint(result_str)
