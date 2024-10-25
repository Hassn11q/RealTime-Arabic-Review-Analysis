from kafka import KafkaConsumer
import json
import psycopg2
from transformers import pipeline

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="postgres",
    port="5432"
)
cur = conn.cursor()

# Connect to Kafka
kafka_nodes = "kafka:9092"
my_topic = "arabic_reviews"

consumer = KafkaConsumer(
    my_topic,
    bootstrap_servers=kafka_nodes,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Load Arabic sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="CAMeL-Lab/bert-base-arabic-camelbert-msa-sentiment")

# Consume messages from the topic
for message in consumer:
    data = message.value
    review = data['review']
    print(f"Received review: {review}")
    
    # Perform sentiment analysis
    result = sentiment_pipeline(review)[0]
    sentiment = result['label']
    score = result['score']
    
    # Map sentiment to Arabic
    arabic_sentiment = "ايجابي" if sentiment == "positive" else "سلبي"
    
    print(f"Sentiment: {arabic_sentiment} (Score: {score})")
    
    # Insert data into PostgreSQL
    cur.execute("INSERT INTO arabic_reviews (review, sentiment, score) VALUES (%s, %s, %s)", 
                (review, arabic_sentiment, score))
    conn.commit()

# Close connections
cur.close()
conn.close()