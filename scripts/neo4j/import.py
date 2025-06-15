#! /bin/python3
from elasticsearch import Elasticsearch
from py2neo import Graph, Node, Relationship


# подключение к ES для перекачки документов
es = Elasticsearch("http://localhost:9200")

# подключение к Neo4j
graph_db = Graph("bolt://localhost:7687", auth=('neo4j', 'iu6-magisters'))

# Запрос чтения всех записей из индекса ES
query = {
  "size": 1000,
  "query": {"match_all": {}}
}

# чтение документов из ES и запись результатов в переменные
response = es.search(index="room", body=query)
room_data = response["hits"]["hits"]
response = es.search(index="clients", body=query)
clients_data = response["hits"]["hits"]

for room in room_data:
    # Создание ноды комнаты
    room_node = Node("Room", Id=room["_id"], Price=room["_source"]["day_price"])
    # Запись ноды комнаты
    graph_db.create(room_node)

for client in clients_data:
    # Создание ноды клиента
    client_node = Node("Client", Id=client["_id"], Arrival=client["_source"]["arriving_date"], Card=client["_source"]["card"])
    # Запись ноды клиента
    graph_db.create(client_node)
    # Поиск ноды комнаты, в которой остановился клиент
    match_query = f"""
        MATCH (r:Room)
        WHERE r.Id = "{client["_source"]["room_id"]}"
        RETURN r as room
    """
    room = graph_db.run(match_query).data()[0]
    # Создание отношения между клиентом и комнатой
    NodesRelationship = Relationship(client_node, "Lived", room["room"], **{"duration": client["_source"]["staying_period"]})
    # Запись отношения между клиентом и комнатой
    graph_db.create(NodesRelationship)


