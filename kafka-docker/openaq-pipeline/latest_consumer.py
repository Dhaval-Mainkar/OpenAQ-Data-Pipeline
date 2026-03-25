from kafka import KafkaConsumer
import boto3
import json
import datetime
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

topic = "air_quality_stream"

bucket = "openaq-project-dm"
prefix = "raw/latest/"

batch_size = 500

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

s3 = boto3.client("s3")

print("Consumer started")

buffer = [] #to hold messages by producer in buffer memory 
seen = set() #makes sure that no duplicate records are added to S3

for message in consumer:

    record = message.value

    try:

        # build unique key
        unique_key = f"{record['locationsId']}_{record['sensorsId']}_{record['datetime']['utc']}"

        # skip duplicates
        if unique_key in seen:
            continue

        seen.add(unique_key)

        buffer.append(record)

        print("Buffered record:", unique_key)

    except Exception as e:
        print("Record parse error:", e)
        continue

    if len(buffer) >= batch_size:

        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        key = f"{prefix}openaq_{timestamp}.json"

        try:

            s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps({"results": buffer})
            )

            print("Uploaded batch:", key)

            buffer = []

        except Exception as e:

            print("S3 upload error:", e)