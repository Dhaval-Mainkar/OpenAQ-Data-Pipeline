from kafka import KafkaConsumer
import boto3
import json
import datetime
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

topic = "air_quality_stream"

bucket = "openaq-project-dm"
prefix = "raw/Sensors/"

batch_size = 500

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

s3 = boto3.client("s3")

print("Sensor consumer started")

buffer = []
seen = set()

for message in consumer:

    record = message.value

    try:

        unique_key = f"{record['id']}_{record['parameter']}"

        if unique_key in seen:
            continue

        seen.add(unique_key)

        buffer.append(record)

        print("Buffered:", unique_key)

    except Exception as e:
        print("Parse error:", e)
        continue


    if len(buffer) >= batch_size:

        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")

        key = f"{prefix}{timestamp}.json"

        try:

            s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps({"results": buffer})
            )

            print("Uploaded:", key)

            buffer = []

        except Exception as e:

            print("S3 error:", e)