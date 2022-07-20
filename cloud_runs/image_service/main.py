import os
from connect import connect, connect_replica
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import json
import sqlalchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)

os.environ['INSTANCE_UNIX_SOCKET'] =  '/cloudsql/innocenceprojectcloud:us-central1:primary'

db = None
db_read = None

@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    global db_read
    db = init_connection_pool()
    db_read = init_connection_pool_replica()

@app.route('/faces')
def getFaces():
    id1 = int(request.args.get('id1'))
    id2 = int(request.args.get('id2'))
    return search_by_range_id(db_read, id1, id2)

@app.route('/face')
def getFace():
    id = int(request.args.get('id'))
    return search_by_id(db_read, id)

@app.route('/save', methods=['POST'])
def insert():
    img = request.form['img']
    return save_image(db, img)
    

def search_by_id(db: sqlalchemy.engine.base.Engine, id):
    stmt = sqlalchemy.text(
        "SELECT img from gen_images WHERE imgID = :id"
    )
    try:
        with db.connect() as conn:
            result = conn.execute(stmt, id=id)
            ans = result.fetchall()
            if len(ans) == 0:
                return jsonify({'img_bytes': None})
            img_bytes = ans[0][0]
    except Exception as e:
        print(e)
        return make_error(400, "Issue when getting image")
    return jsonify({'img_bytes': img_bytes})

def search_by_range_id(db: sqlalchemy.engine.base.Engine, start_id, end_id):
    stmt = sqlalchemy.text(
        "SELECT * from gen_images WHERE imgID >= :start_id AND imgID <= :end_id"
    )
    try:
        with db.connect() as conn:
            result = conn.execute(stmt, start_id=start_id, end_id=end_id)
            ans = result.fetchall()
            ans = list(map(list, zip(*ans)))
            if len(ans) == 0:
                print('Retreived 0 images')
                return jsonify({'imgs_bytes': [], 'ids': []})
            ids = ans[0]
            imgs_bytes = ans[1]
            print('Retreived', len(imgs_bytes), 'images')
    except Exception as e:
        return make_error(400, "Issue when getting image")
    return jsonify({'imgs_bytes': imgs_bytes, 'ids': ids})

def save_image(db: sqlalchemy.engine.base.Engine, b64str: str):
    stmt = sqlalchemy.text(
        "INSERT INTO gen_images (img) VALUES (:img) RETURNING imgID"
    )
    new_id = None
    try:
        with db.connect() as conn:
            result = conn.execute(stmt, img=b64str)
            ans = result.first()
            new_id = ans[0]
    except Exception as e:
        return make_error(400, "Issue when inserting image")
    return jsonify({'id': new_id})

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    return connect()

def init_connection_pool_replica() -> sqlalchemy.engine.base.Engine:
    return connect_replica()

def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'message': message
    })
    response.status_code = status_code
    return response