from flask import Flask, request, render_template
from kafka import KafkaProducer
import pymongo
import json
import os

application = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')


def connect_mongo():
    host = "127.0.0.1:27017"
    db = "faas"
    collection = "function_topic_mapping"
    kafka_collection = "kafka_topics_available"

    url = "mongodb://" + host + "/" + db
    client = pymongo.MongoClient(url)
    db = client[db]
    collection = db[collection]
    kafka_collection = db[kafka_collection]
    return collection, kafka_collection


@application.route('/success')
def success():
   return "Success"


@application.route('/', methods=['POST', 'GET'])
def get_data():
    collection, kafka_collection = connect_mongo()
    topics = kafka_collection.distinct('kafkaTopic')
    if request.method == 'POST':
        task = request.form["task"]
        topic = request.form["topic"]
        data = {
            "task": task,
            "topic": topic
        }
        message = json.dumps(data)
        producer.send(topic, message.encode('utf-8'))
        return render_template("index.html", topics=topics, success="true")
    return render_template("index.html", topics=topics, success="")


if __name__ == '__main__':
    application.run(debug=True)
    producer.close()
