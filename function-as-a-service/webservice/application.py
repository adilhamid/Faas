from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
import os
import sys
import subprocess
sys.path.append("..")

from database.database import Database

app = Flask(__name__)
CORS(app, support_credentials=True)

database = Database()

@app.route('/test')
def test():
    return "This is a test api"


@app.route('/create', methods = ['GET', 'POST'])
def create_function():
    if request.method == 'POST':
        file = request.files['file']
        functionName = request.form['functionName']
        topicName = request.form['kafkaTopic']

        # Checking if the function-name already exists
        functionNamesList = database.getAllFunctionNames()

        if functionName in functionNamesList:
            return "Function name already exists!!!"

    database.insertFunctionEntry(functionName, topicName, file)

    return "File Uploaded Successful"

@app.route('/update', methods = ['GET', 'POST'])
def update_function():
    if request.method == 'POST':
        file = request.files['file']
        functionName = request.form['functionName']

    database.updateEntry(functionName, file)

    return "File Re-Uploaded Successfully"


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
    if request.method == 'GET':
        functionOutput = database.getAllFunctionOutputs()


    return jsonify(results = functionOutput)


@app.route('/createKafkaTopic', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def createKafkaTopic():
    if request.method == 'POST':
        topicName = request.form['kafkaTopicName']

    topicNamesList = database.getAllKafkaTopics()

    if topicName in topicNamesList:
        return "Kafka Topic already exists, please select from drop down items."

    # If Kafka topic doesn't exist
    try:
        subprocess.check_output('kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic ' + topicName, shell=True)
    except:
        e = sys.exc_info()[0]
        print "Exception occured ", e
        return "Kafka topic creation failed"

    database.addKafkaTopic(topicName)

    return 'Kafka Topic created successfully'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3034))
    app.run(debug=True, port=port)
