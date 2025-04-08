from kafka import KafkaProducer
import json
import pandas as pd
import sys

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_data(url):
    df = pd.read_json(url, orient='records', lines=True)

    for _, row in df.head(100).iterrows():
        dict_data = row.to_dict()
        producer.send('games-pg', value=dict_data)
        print(f"Sent: {dict_data}")

    producer.close()

if __name__ == "__main__":
    url = sys.argv[1]
    send_data(url)
