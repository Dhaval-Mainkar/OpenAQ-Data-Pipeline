ssh -i your-key.pem ec2-user@<IPV4 ec2 ip> # Removes all inherited permissions and give read access only to your user

ssh -i your-key.pem ec2-user@<EC2-PUBLIC/PRIVATE-IP> # connect to ec2

# Install Java
sudo yum install java-17-amazon-corretto -y 

sudo yum install java-17-amazon-corretto -y

java -version

# Install kafka
wget https://archive.apache.org/dist/kafka/3.7.0/kafka_2.13-3.7.0.tgz

tar -xvf kafka_2.13-3.7.0.tgz -untar kafka

bin/kafka-storage.sh random-uuid - generate cluster id

bin/kafka-storage.sh format \
-t <PASTE-UUID> \
-c config/kraft/server.properties   -format storage

vi config/kraft/server.properties - open server properties file

#Replaced localhost with ec2 public ip

cd kafka_2.13-3.7.0

#producer
bin/kafka-console-producer.sh \
--topic air_quality_stream \
--bootstrap-server localhost:9092

bootstrap-server localhost:9092 - dry run producer
>hello


#consumer
cd kafka_2.13-3.7.0

bin/kafka-console-consumer.sh \
--topic air_quality_stream \
--bootstrap-server localhost:9092 \
--from-beginning