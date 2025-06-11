source ./settings.sh
sudo docker-compose down
sudo docker-compose up -d --build
#sudo docker exec -i -t $CONTAINER_ELASTIC chmod -R g+w,o+w /scripts/
#sudo docker exec -i -t $CONTAINER_KIBANA systemctl start kibana.service
#sudo docker exec -i -t $CONTAINER_NEO4J /bin/sh -c "/usr/bin/neo4j-admin dbms set-initial-password iu6-magisters"
#sudo docker exec -i -t $CONTAINER_NEO4J service neo4j start
#sudo docker exec -i -t $CONTAINER_SPARK service ssh restart
sudo docker exec -i -t $CONTAINER_PGVECTOR chown -R postgres:postgres /var/lib/postgresql/16/main
sudo docker exec -i -t $CONTAINER_PGVECTOR service postgresql restart
sudo docker exec -i -t $CONTAINER_PGVECTOR chmod -R g+w,o+w /scripts/
sudo docker exec -i -u postgres -t $CONTAINER_PGVECTOR createdb iu6
sudo docker exec -i -u postgres -t $CONTAINER_PGVECTOR psql -d iu6 -c "CREATE EXTENSION vector;"
sudo docker exec -i -u postgres -t $CONTAINER_PGVECTOR psql -c "ALTER USER postgres PASSWORD 'postgres';"
sudo docker exec -i -t --user elasticsearch $CONTAINER_ELASTIC /bin/sh -c "/opt/elasticsearch-7.17.0/bin/elasticsearch"