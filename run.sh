source ./settings.sh
sudo docker-compose down
sudo docker-compose up -d --build
sudo docker exec -i -t $CONTAINER_ELASTIC chmod -R g+w,o+w /scripts/
sudo docker exec -i -t $CONTAINER_KIBANA systemctl start kibana.service
sudo docker exec -i -t --user elasticsearch $CONTAINER_ELASTIC /bin/sh -c "/opt/elasticsearch-7.17.0/bin/elasticsearch"