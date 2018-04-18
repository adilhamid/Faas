from flask import Flask, request
import os
import sys
sys.path.append("..")

from database.database import Database

app = Flask(__name__)

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
        path = "/tmp/"

        print file
        print functionName
        print topicName
        print path

    database.insertFunctionEntry(functionName, topicName, file)

    return "File Uploaded Successful"

@app.route('/edit', methods = ['GET', 'POST'])
def edit_function():
    if request.method == 'GET':
        print "Nothing"

    return "File Uploaded Successful"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3034))
    app.run(debug=True, port=port)