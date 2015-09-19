# coding: utf-8
from flask import Flask, render_template, request
import flask
from model import *
import configinfo
app = Flask(__name__)
events_model = PubSubModel()

def event_stream():
    '''
    create a stream from the published information in the redis database
    :return:
    '''
    pubsub = events_model.get_publisher()
    pubsub.subscribe(configinfo.event_stream_name)
    for event in pubsub.listen():
        yield 'data: %s\n\n' % event[configinfo.data_name]

@app.route('/stream')
def stream():
    '''
    :return: a data stream from the event model
    '''
    return flask.Response(event_stream(), mimetype='text/event-stream')

@app.route('/api/push/', methods=["POST"])
def insert_event():
    print "pushing data"
    data = json.loads(request.data)
    print data
    events_model.publish_event(data)
    return "OK"

@app.route('/api/config/room', methods = ["POST"])
def insert_room():
    print "inserting room"
    data = json.loads(request.data)
    events_model.set_room(data['sensor_id'], data['room'])
    return "OK"

@app.route('/api/config')
def config():
    return render_template('config.html')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=True)
