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
        f = request.files['file']
        functionName = request.form['functionName']
        topicName = request.form['kafkaTopic']

    database.insertFunctionEntry(functionName, topicName, f)

    return "File Uploaded Successful"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3034))
    app.run(debug=True, port=port)