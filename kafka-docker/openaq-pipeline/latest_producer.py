from kafka import KafkaProducer
import boto3
import json
import requests
import time
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

API_KEY = os.getenv("OPENAQ_API_KEY")

headers = {
    "X-API-Key": API_KEY
}

bucket = "openaq-project-dm"
raw_prefix = "raw/locations/"
topic = "air_quality_stream"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

s3 = boto3.client("s3")

response = s3.list_objects_v2(
    Bucket=bucket,
    Prefix=raw_prefix
)

files = [
    obj["Key"]
    for obj in response.get("Contents", [])
    if obj["Key"].endswith(".json")
]

print("Raw files found:",len(files))

location_ids = set() #makes sure that no location is repeated that was already present in S3

for file in files:

    obj = s3.get_object(Bucket=bucket, Key=file)

    data = json.loads(obj["Body"].read())

    for r in data.get("results", []):
        if "id" in r:
            location_ids.add(r["id"])

print("Unique location IDs:", len(location_ids))

for loc_id in location_ids:

    url = f"https://api.openaq.org/v3/locations/{loc_id}/latest"

    print("Calling API:", url)

    retries = 3

    while retries > 0:

        try:

            r = requests.get(url, headers=headers)

            # HANDLE RATE LIMIT

            if r.status_code == 429:
                print("Rate limit hit. Sleeping 10 seconds...")
                time.sleep(10)
                retries -= 1
                continue

            if r.status_code != 200:
                print("API error:", r.text)
                break

            api_data = r.json()

            results = api_data.get("results", [])

            for record in results:
                producer.send(topic, record)

            print("Records sent:", len(results))

            break

        except Exception as e:
            print("Request failed:", e)
            retries -= 1
            time.sleep(5)

    # small delay to avoid hitting rate limits
    time.sleep(1)
    
producer.flush()

print("Producer finished streaming data to Kafka")