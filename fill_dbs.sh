source ./settings.sh
sudo docker exec -i -t $CONTAINER_ELASTIC /bin/sh -c "/scripts/import_elastic.py"
sudo docker exec -i -t $CONTAINER_NEO4J /bin/sh -c "/scripts/import.py"