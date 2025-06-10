#! /bin/python3
from pyspark.sql import SparkSession

sparkSession = SparkSession.builder.appName("DBCourse").getOrCreate()

living_df = sparkSession.read.csv(
            "hdfs://localhost:9000/DBCourse/living.csv",
            header=True,
            inferSchema=True
        )
        
room_df = sparkSession.read.csv(
    "hdfs://localhost:9000/DBCourse/room.csv",
    header=True,
    inferSchema=True
)

living_df.createOrReplaceTempView("living")
room_df.createOrReplaceTempView("rooms")

result = sparkSession.sql(
"""
  SELECT 
      r.Id as Room_id,
      r.Description,
      r.Day_price,
      COUNT(l.Room_id) as total_stays
  FROM living l
  JOIN rooms r ON l.Room_id = r.Id
  GROUP BY r.Id, r.Description, r.Day_price
  ORDER BY total_stays DESC
""")

result.show()
input() #to check monitorings at http://127.0.0.1:4040/jobs/