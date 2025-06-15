#! /bin/python3
from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, Row
from datetime import datetime

# подключение к ES для перекачки документов
es = Elasticsearch("http://localhost:9200")
# подключение к HDFS
sparkSession = SparkSession.builder.appName("DBCourse").getOrCreate()

# Запрос чтения всех записей из индекса ES
query = {
  "size": 1000,
  "query": {"match_all": {}}
}

# Схема csv файла комнат
RoomSchema = StructType([
StructField("Id", IntegerType(), False),
StructField("Description", StringType(), False),
StructField("Day_price", IntegerType(), False),
])
# Схема csv файла клиентов
ClientSchema = StructType([
StructField("Id", IntegerType(), False),
StructField("Card", StringType(), False),
])
# Схема csv файла проживания
LivingSchema = StructType([
StructField("Id", IntegerType(), False),
StructField("Client_id", IntegerType(), False),
StructField("Room_id", IntegerType(), False),
StructField("Arriving_date", DateType(), False),
StructField("Staying_period", IntegerType(), False),
StructField("Services", StringType(), False)
])

# чтение документов из ES и запись результатов в переменные
response = es.search(index="room", body=query)
room_data = response["hits"]["hits"]
response = es.search(index="clients", body=query)
clients_data = response["hits"]["hits"]

data_client = []
data_living = []
for client in clients_data:
    # создание записи клиента 
    client_line = (int(client["_source"]["client_id"]), client["_source"]["card"].replace("\n", " "))
    # создание записи проживание
    living_line = (int(client["_id"]),int(client["_source"]["client_id"]), int(client["_source"]["room_id"]), datetime.strptime(client["_source"]["arriving_date"], "%Y-%m-%d"), int(client["_source"]["staying_period"]), client["_source"]["services"])
    # добавление записей в общий список для bulk записи в БД
    data_client.append(client_line)
    data_living.append(living_line)

data = []
for room in room_data:
     # создание записи комнаты 
    room_line = Row(Id=int(room["_id"]), Description=room["_source"]["description"].replace("\n", " "), Day_price=int(room["_source"]["day_price"]))
    # добавление записи в общий список для bulk записи в БД
    data.append(room_line)

#создание DataFrame и запись их в HDFS
df = sparkSession.createDataFrame(data_client, ClientSchema)
df.write.csv("hdfs://localhost:9000/DBCourse/client.csv", mode='overwrite', header=True)
df = sparkSession.createDataFrame(data_living, LivingSchema)
df.write.csv("hdfs://localhost:9000/DBCourse/living.csv", mode='overwrite', header=True)
df = sparkSession.createDataFrame(data, schema=RoomSchema)
df.write.csv("hdfs://localhost:9000/DBCourse/room.csv", mode='overwrite', header=True)

# Вывод результатов для проверки
print("Room:")
df_load = sparkSession.read.csv('hdfs://localhost:9000/DBCourse/room.csv')
df_load.show()

print("Client:")
df_load = sparkSession.read.csv('hdfs://localhost:9000/DBCourse/client.csv')
df_load.show()

print("Living:")
df_load = sparkSession.read.csv('hdfs://localhost:9000/DBCourse/living.csv')
df_load.show()
