# Enter container and start producer
docker exec -it kafka bash

/opt/kafka/bin/kafka-console-producer.sh \
  --topic air_quality_stream \
  --bootstrap-server localhost:9092

# Then type a demo message for testing