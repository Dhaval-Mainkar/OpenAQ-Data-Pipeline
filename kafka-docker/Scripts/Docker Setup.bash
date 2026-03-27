#Start Kafka container
docker compose up -d

# To verify Kafka is running
docker ps

# Enter the Kafka container
docker exec -it kafka bash

cd /opt/kafka

# Create Kafka topic
/opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic air_quality_stream \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# Verify topic was created
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
exit

# List all topics
docker exec -it kafka bash -c "/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092"

# Describe a topic
docker exec -it kafka bash -c "/opt/kafka/bin/kafka-topics.sh --describe --topic air_quality_stream --bootstrap-server localhost:9092"