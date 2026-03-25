from kafka import KafkaProducer
import boto3
import json
import requests
import time
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

topic = "air_quality_stream"

bucket = "openaq-project-dm"
prefix = "raw/latest/"

API_KEY = os.getenv("OPENAQ_API_KEY")

headers = {
    "X-API-Key": API_KEY
}

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

s3 = boto3.client("s3")

response = s3.list_objects_v2(
    Bucket=bucket,
    Prefix=prefix
)

files = [
    obj["Key"]
    for obj in response.get("Contents", [])
    if obj["Key"].endswith(".json")
]

print("Latest files:", len(files))

location_ids = set()

for file in files:

    obj = s3.get_object(Bucket=bucket, Key=file)

    data = json.loads(obj["Body"].read())

    for r in data.get("results", []):

        if "locationsId" in r:
            location_ids.add(r["locationsId"])

print("Unique locations:", len(location_ids))

for loc_id in location_ids:

    url = f"https://api.openaq.org/v3/sensors/{loc_id}"

    print("Calling:", url)

    try:

        r = requests.get(url, headers=headers)

        if r.status_code == 429:
            print("Rate limit hit")
            time.sleep(10)
            continue

        if r.status_code != 200:
            print("API error:", r.text)
            continue

        data = r.json()

        for record in data.get("results", []):

            producer.send(topic, record)

        print("Records sent:", len(data.get("results", [])))

        time.sleep(1)

    except Exception as e:

        print("Producer error:", e)

producer.flush()

print("Sensor producer finished")