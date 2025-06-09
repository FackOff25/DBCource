#! /bin/python3
from elasticsearch import Elasticsearch
from py2neo import Graph, Node, Relationship

ng=200

#the index client used to communicate with the database
es = Elasticsearch("http://localhost:9200")
#the index name
indexName = "clients"
docType = 'recipes'

graph_db = Graph("bolt://localhost:7687", auth=('neo4j', 'iu6-magisters'))

query = {
  "size": 1000,
  "query": {"match_all": {}}
}

response = es.search(index="room", body=query)
room_data = response["hits"]["hits"]
for room in room_data:
    room_node = Node("Room", Id=room["_id"], Price=room["_source"]["day_price"])
    #graph_db.create(room_node)

response = es.search(index="clients", body=query)
clients_data = response["hits"]["hits"]

for client in clients_data:
    client_node = Node("Client", Id=client["_id"], Arrival=client["_source"]["arriving_date"], Card=client["_source"]["card"])
    graph_db.create(client_node)
    match_query = f"""
        MATCH (r:Room)
        WHERE r.Id = "{client["_source"]["room_id"]}"
        RETURN r as room
    """
    print(client)
    room = graph_db.run(match_query).data()[0]
    NodesRelationship = Relationship(client_node, "Lived", room["room"], **{"duration": client["_source"]["staying_period"]})
    graph_db.create(NodesRelationship)


