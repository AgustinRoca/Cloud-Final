from time import sleep
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from google.cloud import pubsub_v1
from google.api_core import retry
import json
from json_serializer import NumpyArrayEncoder

app = Flask(__name__)

app.config["DEBUG"] = True #If the code is malformed, there will be an error shown when visit app
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

CORS(app)

pub = pubsub_v1.PublisherClient()
topic_path = 'projects/innocenceprojectcloud/topics/task'

subscription_path = 'projects/innocenceprojectcloud/subscriptions/task_response-sub'

def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'message': message
    })
    response.status_code = status_code
    return response

@app.route('/hello')
def home():
    return jsonify({'msg': 'hello! :)'})

@app.route('/faces', methods=['POST'])
def generateFaces():
    amount = request.form['amount']
    if amount is not None:
        amount = int(amount)
    else:
        amount = 1

    data = f'faces;{amount}'
    data = data.encode('utf-8')

    future = pub.publish(topic_path, data)
    message_id = str(future.result())
    print(f'Message {message_id} published for GCE to process')

    return get_response_message(message_id)


@app.route('/transition', methods=['POST'])
def generateTransition():
    id1 = int(request.form['id1'])
    id2 = int(request.form['id2'])
    amount = int(request.form['amount'])

    data = f'transition;{id1};{id2};{amount}'
    data = data.encode('utf-8')

    future = pub.publish(topic_path, data)
    message_id = str(future.result())
    print(f'Message {message_id} published for GCE to process')

    return get_response_message(message_id)   

@app.route('/latentspace', methods=['POST'])
def image_to_latent_space():
    base64str = request.form['file']
    data = f'latentspace;{base64str}'
    data = data.encode('utf-8')

    future = pub.publish(topic_path, data)
    message_id = str(future.result())
    print(f'Message {message_id} published for GCE to process')

    return get_response_message(message_id)   

@app.route('/features', methods=['POST'])
def change_features():
    ageAmount = request.form['ageAmount']
    if ageAmount == '':
        ageAmount = 0
    eyeDistanceAmount = request.form['eyeDistanceAmount']
    if eyeDistanceAmount == '':
        eyeDistanceAmount = 0
    eyeEyebrowDistanceAmount = request.form['eyeEyebrowDistanceAmount']
    if eyeEyebrowDistanceAmount == '':
        eyeEyebrowDistanceAmount = 0
    eyeRatioAmount = request.form['eyeRatioAmount']
    if eyeRatioAmount == '':
        eyeRatioAmount = 0
    eyesOpenAmount = request.form['eyesOpenAmount']
    if eyesOpenAmount == '':
        eyesOpenAmount = 0
    genderAmount = request.form['genderAmount']
    if genderAmount == '':
        genderAmount = 0
    lipRatioAmount = request.form['lipRatioAmount']
    if lipRatioAmount == '':
        lipRatioAmount = 0
    mouthOpenAmount = request.form['mouthOpenAmount']
    if mouthOpenAmount == '':
        mouthOpenAmount = 0
    mouthRatioAmount = request.form['mouthRatioAmount']
    if mouthRatioAmount == '':
        mouthRatioAmount = 0
    noseMouthDistanceAmount = request.form['noseMouthDistanceAmount']
    if noseMouthDistanceAmount == '':
        noseMouthDistanceAmount = 0
    noseRatioAmount = request.form['noseRatioAmount']
    if noseRatioAmount == '':
        noseRatioAmount = 0
    noseTipAmount = request.form['noseTipAmount']
    if noseTipAmount == '':
        noseTipAmount = 0
    pitchAmount = request.form['pitchAmount']
    if pitchAmount == '':
        pitchAmount = 0
    rollAmount = request.form['rollAmount']
    if rollAmount == '':
        rollAmount = 0
    smileAmount = request.form['smileAmount']
    if smileAmount == '':
        smileAmount = 0
    yawAmount = request.form['yawAmount']
    if yawAmount == '':
        yawAmount = 0
    id = request.form['id']

    data = f'features;{id};{ageAmount};{eyeDistanceAmount};{eyeEyebrowDistanceAmount};{eyeRatioAmount};{eyesOpenAmount};{genderAmount};{lipRatioAmount};{mouthOpenAmount};{mouthRatioAmount};{noseMouthDistanceAmount};{noseRatioAmount};{noseTipAmount};{noseTipAmount};{pitchAmount};{rollAmount};{smileAmount};{yawAmount}'
    data = data.encode('utf-8')

    future = pub.publish(topic_path, data)
    message_id = str(future.result())
    print(f'Message {message_id} published for GCE to process')

    return get_response_message(message_id)

@app.route('/interchange', methods=['POST'])
def mix_styles():
    id1 = int(request.form['id1'])
    id2 = int(request.form['id2'])
    
    data = f'interchange;{id1};{id2}'
    data = data.encode('utf-8')

    future = pub.publish(topic_path, data)
    message_id = str(future.result())
    print(f'Message {message_id} published for GCE to process')

    return get_response_message(message_id)

def get_response_message(message_id):
    subscriber = pubsub_v1.SubscriberClient()

    NUM_MESSAGES = 3

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        # The subscriber pulls a specific number of messages. The actual
        # number of messages pulled may be smaller than max_messages.
        done = False
        while not done:
            response = subscriber.pull(
                request={"subscription": subscription_path, "max_messages": NUM_MESSAGES},
                retry=retry.Retry(deadline=300),
            )

            if len(response.received_messages) != 0:
                ack_ids = []
                for received_message in response.received_messages:
                    if received_message.message.attributes.get('id') == message_id:
                        print(f"Received: {received_message.message.data}.")
                        ack_ids.append(received_message.ack_id)
                        response = received_message.message.data
                        done = True
                        subscriber.acknowledge(
                            request={"subscription": subscription_path, "ack_ids": ack_ids}
                        )
                    else:
                        print(f'Message not directed to the message I published: {message_id}')
                        id_got = received_message.message.attributes.get('id')
                        print(f'ID: {id_got}')
            else:
                sleep(5)
    ans = json.loads(response.decode('utf-8'))
    if 'error' in ans:
        return make_error(404, 'Invalid message')
    return jsonify(ans) 