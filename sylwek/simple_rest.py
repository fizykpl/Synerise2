import json

from flask import Flask,jsonify
from kafka import KafkaProducer
from sylwek.data_provider import DataProvider

app = Flask(__name__)
dp = DataProvider()


def send_to_kafka(topic, msg):
    print('Send Event to Kafka:')
    # producer.send(topic, msg)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/most_similar/<int:image_id>/<int:top_limit>')
def most_similar(image_id,top_limit):
    print('most_similar')
    topic = 'most_similar'
    msg = ('{} {}'.format(image_id,top_limit))
    send_to_kafka(topic,msg)
    output = dp.similarity_measure.most_similar(image_id,top_limit)
    return jsonify({'most_similar':output})

@app.route('/total_count_images')
def total_count_images():
    topic = 'total_count_id'
    msg = 'event'
    send_to_kafka(topic,msg)
    output = len(dp.images)
    return jsonify({'total_count_id':output})

@app.route('/total_count_labels')
def total_count_labels():
    topic = 'total_count_labels'
    msg = 'event'
    send_to_kafka(topic,msg)
    output = {}
    for label in dp.labels:
        output[str(label)] = len(dp.labels[label])
    output = json.dumps(output)
    return jsonify({'total_count_id':output})

if __name__ == '__main__':
    app.run(port=8081)