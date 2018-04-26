from flask import Flask, request, jsonify, redirect
from flask_cors import cross_origin, CORS
import os
import sys
import json
import subprocess
sys.path.append("..")

from database.database import Database

app = Flask(__name__)
CORS(app, support_credentials=True)

database = Database()

WEBAPP_HOSTNAME = "http://localhost:63342/689-18-a-P2/webapp/"

@app.route('/test')
def test():
    return "This is a test api"


@app.route('/create', methods = ['GET', 'POST'])
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

    database.insertFunctionEntry(functionName, topicName, file)

    return redirect(WEBAPP_HOSTNAME + '/create.html?status=3')

@app.route('/update', methods = ['GET', 'POST'])
def update_function():
    if request.method == 'POST':
        file = request.files['file']
        functionName = request.form['functionName']
        fileName = file.filename

        # Checking if the file is a python file
        if fileName.split(".")[-1] != "py":
            return redirect(WEBAPP_HOSTNAME + '/edit.html?status=1')

    database.updateEntry(functionName, file)

    return redirect(WEBAPP_HOSTNAME + '/edit.html?status=0')


@app.route('/getFunctionName', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getFunctionNames():
    if request.method == 'GET':
        functionNames = database.getAllFunctionNames()

    return jsonify(array=functionNames)

@app.route('/getTopicNames', methods = ['GET'])
@cross_origin(supports_credentials=True)
def getTopicNames():
    if request.method == 'GET':
        topicNames = database.getAllKafkaTopics()

    return jsonify(array=topicNames)


@app.route('/getFunctionOutput', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getFunctionOutputs():
    result =[]
    if request.method == 'GET':
        functionOutput = database.getAllFunctionOutputs()

        for item in functionOutput:
            result.append({"timestamp": item["timestamp"], "functionName": item["functionName"],
                           "userData": item["userData"], "outputResult": item["outputResult"]})

    return jsonify(array=result)


@app.route('/createKafkaTopic', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def createKafkaTopic():
    topicName = request.form['kafkaTopicName']

    topicNamesList = database.getAllKafkaTopics()

    if topicName in topicNamesList:
        return redirect(WEBAPP_HOSTNAME + '/create.html?status=2')

    # If Kafka topic doesn't exist
    try:
        subprocess.check_output('kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic ' + topicName, shell=True)
    except:
        e = sys.exc_info()[0]
        print "Exception occured ", e
        redirect(WEBAPP_HOSTNAME + '/create.html?status=0')

    database.addKafkaTopic(topicName)

    return redirect(WEBAPP_HOSTNAME + '/create.html?status=1')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3034))
    app.run(debug=True, port=port)
