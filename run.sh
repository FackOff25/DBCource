source ./settings.sh
sudo docker-compose down
sudo docker-compose up -d --build
sudo docker exec -i -t $CONTAINER chmod -R g+w,o+w /scripts/
sudo docker exec -i -t --user elasticsearch $CONTAINER /bin/sh -c "/opt/elasticsearch-7.17.0/bin/elasticsearch"