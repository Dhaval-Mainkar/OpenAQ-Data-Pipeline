# In a new terminal start consumer
docker exec -it kafka bash

/opt/kafka/bin/kafka-console-consumer.sh \
  --topic air_quality_stream \
  --bootstrap-server localhost:9092 \
  --from-beginning

# Read only a fixed number of messages
/opt/kafka/bin/kafka-console-consumer.sh \
  --topic air_quality_stream \
  --bootstrap-server localhost:9092 \
  --from-beginning \
  --max-messages 10

# Exit after 5 seconds of inactivity

/opt/kafka/bin/kafka-console-consumer.sh \
  --topic air_quality_stream \
  --bootstrap-server localhost:9092 \
  --from-beginning \
  --timeout-ms 5000