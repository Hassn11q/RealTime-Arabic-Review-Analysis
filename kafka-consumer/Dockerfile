FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it.sh for waiting for dependencies (Kafka, Zookeeper)
COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

# Copy the main Python file
COPY consumer.py .

# Define environment variables
ENV KAFKA_NODES=kafka:9092
ENV TOPIC_NAME=arabic_reviews

# Command to run the consumer
CMD ./wait-for-it.sh -s -t 30 $KAFKA_NODES -- python consumer.py