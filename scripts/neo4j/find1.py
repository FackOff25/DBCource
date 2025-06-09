#! /bin/python3
from py2neo import Graph, Node, Relationship

graph_db = Graph("bolt://localhost:7687", auth=('neo4j', 'iu6-magisters'))

match_query = f"""
        MATCH (c:Client)-[rel:Lived]->(r:Room)
        WITH c, rel, r, rel.duration * r.Price AS total_cost
        ORDER BY total_cost DESC
        LIMIT 1
        RETURN c.Id AS client_id, 
            c.Card AS card,
            total_cost,
            rel.duration AS days,
            r.Price AS day_price
    """
client = graph_db.run(match_query).data()[0]
print(client)
