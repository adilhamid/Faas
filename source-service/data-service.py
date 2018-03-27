from flask import Flask, jsonify
from kafka import KafkaProducer

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')


@app.route('/source/<task>', methods=['GET'])
def get_data(task):
    producer.send('my-topic', task.encode())
    return jsonify(task)


if __name__ == '__main__':
    app.run(debug=True)
    producer.close()