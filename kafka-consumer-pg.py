from kafka import KafkaConsumer
import json
import psycopg2

print('🔄 Conectando a PostgreSQL...')

try:
    conn = psycopg2.connect(
        database="defaultdb",
        user="avnadmin",
        host="pg-1aa56d3f-rodrigo413.h.aivencloud.com",
        password="AVNS_SeUblJcKtl3naJLVcKs",
        port=15385
    )
    cur = conn.cursor()
    print("✅ PostgreSQL conectado exitosamente!")
except Exception as e:
    print(f"❌ Error al conectar a PostgreSQL: {e}")

consumer = KafkaConsumer(
    'games-pg',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for msg in consumer:
    record = msg.value
    title = record.get("title")
    console = record.get("console")

    try:
        sql = "INSERT INTO games (title, console) VALUES (%s, %s)"
        cur.execute(sql, (title, console))
        conn.commit()
        print(f"✅ Insertado: {title} - {console}")
    except Exception as e:
        print(f"❌ Error al insertar en PostgreSQL: {e}")

conn.close()
