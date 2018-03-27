from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
consumer.subscribe(['my-topic'])

while True:
    for message in consumer:
        print message.value
