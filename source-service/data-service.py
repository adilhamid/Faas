from flask import Flask, redirect, url_for, request, render_template
from kafka import KafkaProducer

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')


@app.route('/success')
def success():
   return "Success"


@app.route('/', methods=['POST', 'GET'])
def get_data():

    if request.method == 'POST':
        task = request.form["task"]
        producer.send('function1', task.encode('utf-8'))
        return redirect(url_for('success'))

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
    producer.close()
