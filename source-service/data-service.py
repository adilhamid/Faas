from flask import Flask, request, render_template
from kafka import KafkaProducer
import pymongo
import json


app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')


def connect_mongo():
    host = "127.0.0.1:27017"
    db = "faas"
    collection = "function_topic_mapping"
    url = "mongodb://" + host + "/" + db
    client = pymongo.MongoClient(url)
    db = client[db]
    collection = db[collection]
    return collection


@app.route('/success')
def success():
   return "Success"


@app.route('/', methods=['POST', 'GET'])
def get_data():
    collection = connect_mongo()
    topics = collection.distinct('topicName')
    if request.method == 'POST':
        task = request.form["task"]
        topic = request.form["topic"]
        data = {
            "task": task,
            "topic": topic
        }
        message = json.dumps(data)
        producer.send(topic, message.encode('utf-8'))
        return render_template("index.html", topics=topics)
    return render_template("index.html", topics=topics)


if __name__ == '__main__':
    app.run(debug=True)
    producer.close()
