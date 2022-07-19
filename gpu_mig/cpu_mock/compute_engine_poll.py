from time import sleep
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import json

from mock_functions import *

def main():
    # timeout = 5.0

    sub = pubsub_v1.SubscriberClient()
    subscrption_path = 'projects/innocenceprojectcloud/subscriptions/task-sub'

    flow_control =  pubsub_v1.types.FlowControl(max_messages=1)
    streaming_pull_future = sub.subscribe(subscrption_path, callback=callback, flow_control=flow_control)
    print('Subscribed')
    with sub:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()

def callback(message):
        data = message.data.decode("utf-8")
        print(message)
        message_id = message.message_id
        message.ack()
        if data.startswith('faces'):
            imgs_bytes, zs = faces(data)
            response = {'imgs_bytes': imgs_bytes, 'zs': zs}
            json_response = json.dumps(response)

        elif data.startswith('transition'):
            transition(data)
        elif data.startswith('latentspace'):
            latentspace(data)
        elif data.startswith('features'):
            features(data)
        elif data.startswith('interchange'):
            interchange(data)
        else:
            error(data)

        pub = pubsub_v1.PublisherClient()
        topic_path = 'projects/innocenceprojectcloud/topics/task_response'
        data = f'{json_response}'
        data = data.encode('utf-8')
        future = pub.publish(topic_path, data, id=message_id)
        future.result()

def faces(data):
    args = data.split(';')
    return generate_random_faces(int(args[1]))


def transition(data):
    args = data.split(';')
    generate_transition(int(args[1]), int(args[2]), int(args[3]))
    sleep(2)

def latentspace(data):
    args = data.split(';')
    base64_to_latent(args[1])
    sleep(20)

def features(data):
    args = data.split(';')
    features_dict = {}
    id = args[1]
    features_dict['age'] = float(args[2])
    features_dict['eye_distance'] = float(args[3])
    features_dict['eye_eyebrow_distance'] = float(args[4])
    features_dict['eye_ratio'] = float(args[5])
    features_dict['eyes_open'] = float(args[6])
    features_dict['gender'] = float(args[7])
    features_dict['lip_ratio'] = float(args[8])
    features_dict['mouth_open'] = float(args[9])
    features_dict['mouth_ratio'] = float(args[10])
    features_dict['nose_mouth_distance'] = float(args[11])
    features_dict['nose_ratio'] = float(args[12])
    features_dict['nose_tip'] = float(args[13])
    features_dict['pitch'] = float(args[14])
    features_dict['roll'] = float(args[15])
    features_dict['smile'] = float(args[16])
    features_dict['yaw'] = float(args[17])

    change_features(id, features_dict)
    sleep(2)

def interchange(data):
    args = data.split(';')
    mix_styles(args[1], args[2])
    sleep(1)

def error(data):
    sleep(1)

if __name__ == "__main__":
    main()
