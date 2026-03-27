# Navigate to kakfa-docker folder
cd C:\Users\admin\Desktop\Test\kafka-docker\openaq-pipeline

# Build the Docker image
docker build -t openaq-pipeline .

# Verify the image was created
docker images

# Run Latest Producer
docker run -it \
  -v %USERPROFILE%\.aws:/root/.aws \
  -e AWS_DEFAULT_REGION=<YOUR_REGION> \
  -e KAFKA_SERVER=host.docker.internal:9092 \
  -e OPENAQ_API_KEY=YOUR_API_KEY \
  openaq-pipeline python -u latest_producer.py

# Run Latest Consumer
docker run -it \
  -v %USERPROFILE%\.aws:/root/.aws \
  -e AWS_DEFAULT_REGION=<YOUR_REGION>\
  -e KAFKA_SERVER=host.docker.internal:9092 \
  openaq-pipeline python -u latest_consumer.py

# Run Sensor Producer
docker run -it \
  -v %USERPROFILE%\.aws:/root/.aws \
  -e AWS_DEFAULT_REGION=<YOUR_REGION> \
  -e KAFKA_SERVER=host.docker.internal:9092 \
  -e OPENAQ_API_KEY=YOUR_API_KEY \
  openaq-pipeline python -u sensor_producer.py

# Run Sensor Consumer
docker run -it \
  -v %USERPROFILE%\.aws:/root/.aws \
  -e AWS_DEFAULT_REGION=<YOUR_REGION>\
  -e KAFKA_SERVER=host.docker.internal:9092 \
  openaq-pipeline python -u sensor_consumer.py

# Check running containers
docker ps
 
# Check all containers including exited ones
docker ps -a
 
# View logs of a specific container (use container ID from docker ps -a)
docker logs <container_id>
 
# Remove all stopped containers (cleanup)
docker container prune
 
# Open a bash shell inside the pipeline container for manual debugging
docker run -it \
  -v %USERPROFILE%\.aws:/root/.aws \
  openaq-pipeline bash

# To Authenticate Docker to your ECR registry
aws ecr get-login-password --region <YOUR_REGION> | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.<YOUR_REGION>.amazonaws.com

# Tag local image for ECR
docker tag openaq-pipeline:latest YOUR_ACCOUNT_ID.dkr.ecr.<YOUR_REGION>.amazonaws.com/openaq-pipeline:latest
 
# Push image to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.<YOUR_REGION>.amazonaws.com/openaq-pipeline:latest

# Start Kafka on EC2 instance
docker compose up -d

# Start Consumer
docker run -it -v %USERPROFILE%\.aws:/root/.aws -e AWS_DEFAULT_REGION=<YOUR_REGION> -e KAFKA_SERVER=host.docker.internal:9092 openaq-pipeline python -u latest_consumer.pyStart Consumer

# Start Producer (in a separate terminal)
docker run -it -v %USERPROFILE%\.aws:/root/.aws -e AWS_DEFAULT_REGION=<YOUR_REGION> -e KAFKA_SERVER=host.docker.internal:9092 -e OPENAQ_API_KEY=YOUR_API_KEY openaq-pipeline python -u latest_producer.py

# Monitor Kafka topic in real time
docker exec -it kafka bash -c "/opt/kafka/bin/kafka-console-consumer.sh --topic air_quality_stream --bootstrap-server localhost:9092 --from-beginning"

# Reset Kafka Container in EC2
docker compose down -v