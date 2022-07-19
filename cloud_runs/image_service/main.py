from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from google.oauth2 import service_account

# from json_serializer import NumpyArrayEncoder

app = Flask(__name__)

app.config["DEBUG"] = True #If the code is malformed, there will be an error shown when visit app
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

CORS(app)

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

# ---

# @app.route('/faces')
# def getFaces():
#     id1 = int(request.args.get('id1'))
#     id2 = int(request.args.get('id2'))
#     imgs_bytes, ids = service.get_images_from_database(id1, id2)
#     return jsonify({'ids': ids, 'imgs_bytes': imgs_bytes})

# @app.route('/save', methods=['POST'])
# def save_latent_code():
#     z = request.form['z']
#     z = z.split(',')
#     z = [float(num) for num in z]
#     z = np.array(z)
#     z = z.reshape((1,18,512))
#     id = service.save_image(z)
#     jsonData = {'id': id}
#     return json.dumps(jsonData, cls=NumpyArrayEncoder)   