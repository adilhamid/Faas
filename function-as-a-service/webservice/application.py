from flask import Flask, request, jsonify, redirect
from flask_cors import cross_origin, CORS
import os
import sys
from kafka.client import KafkaClient
from kafka import KafkaProducer
sys.path.append("..")

from util.config import Config
from database.database import Database

application = Flask(__name__)
CORS(application, support_credentials=True)

database = Database()

config = Config()
WEBAPP_HOSTNAME = config.ADMIN_WEBAPP_HOSTNAME
client = KafkaClient(bootstrap_servers=config.KAFKA_QUEUE_HOSTNAME_PORT)
producer = KafkaProducer(bootstrap_servers=config.KAFKA_QUEUE_HOSTNAME_PORT)

@application.route('/test')
def test():
    return "This is a test api"


@application.route('/create', methods = ['GET', 'POST'])
def create_function():
    if request.method == 'POST':
        file = request.files['file']
        functionName = request.form['functionName']
        topicName = request.form['kafkaTopic']
        fileName = file.filename

        # Checking if the file is a python file
        if fileName.split(".")[-1] != "py":
            return redirect(WEBAPP_HOSTNAME + '/create.html?status=4')

        # Checking if the function-name already exists
        functionNamesList = database.getAllFunctionNames()

        if functionName in functionNamesList:
            return redirect(WEBAPP_HOSTNAME + '/create.html?status=5')
    try:
        database.insertFunctionEntry(functionName, topicName, file)
        return redirect(WEBAPP_HOSTNAME + '/create.html?status=3')
    except:
        return redirect(WEBAPP_HOSTNAME + '/create.html?status=6')


@application.route('/update', methods = ['GET', 'POST'])
def update_function():
    if request.method == 'POST':
        file = request.files['file']
        functionName = request.form['functionName']
        fileName = file.filename

        # Checking if the file is a python file
        if fileName.split(".")[-1] != "py":
            return redirect(WEBAPP_HOSTNAME + '/edit.html?status=1')

    try:
        database.updateEntry(functionName, file)
        return redirect(WEBAPP_HOSTNAME + '/edit.html?status=0')
    except:
        return redirect(WEBAPP_HOSTNAME + '/edit.html?status=2')





@application.route('/getFunctionName', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getFunctionNames():
    if request.method == 'GET':
        functionNames = database.getAllFunctionNames()

    return jsonify(array=functionNames)

@application.route('/getTopicNames', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getTopicNames():
    if request.method == 'GET':
        topicNames = database.getAllKafkaTopics()

    return jsonify(array=topicNames)


@application.route('/getFunctionOutput', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getFunctionOutputs():
    result =[]
    if request.method == 'GET':
        functionOutput = database.getAllFunctionOutputs()

        for item in functionOutput:
            result.append({"timestamp": item["timestamp"], "functionName": item["functionName"],
                           "userData": item["userData"], "outputResult": item["outputResult"]})

    return jsonify(array=result)


@application.route('/createKafkaTopic', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def createKafkaTopic():
    topicName = request.form['kafkaTopicName']

    topicNamesList = database.getAllKafkaTopics()

    if topicName in topicNamesList:
        return redirect(WEBAPP_HOSTNAME + '/create.html?status=2')

    # If Kafka topic doesn't exist
    try:
        client.add_topic(topicName)
    except:
        e = sys.exc_info()[0]
        print "Exception occured ", e
        redirect(WEBAPP_HOSTNAME + '/create.html?status=0')

    database.addKafkaTopic(topicName)
    producer.send(topicName, "test".encode('utf-8'))

    return redirect(WEBAPP_HOSTNAME + '/create.html?status=1')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3034))
    application.run(debug=True, port=port)
