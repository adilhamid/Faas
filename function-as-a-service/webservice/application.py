from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
import os
import sys
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

    database.insertFunctionEntry(functionName, topicName, file)

    return "File Uploaded Successful"


@app.route('/getFunctionName', methods = ['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getFunctionNames():
    if request.method == 'POST':
        functionNames = database.getAllFunctionNames()

    return jsonify(array=functionNames)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3034))
    app.run(debug=True, port=port)
