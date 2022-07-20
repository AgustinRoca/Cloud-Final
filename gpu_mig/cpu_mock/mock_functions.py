from time import sleep
import base64
from io import BytesIO
import os
from PIL import Image
import numpy as np
from connect import connect_replica
import sqlalchemy

def generate_random_faces(amount):
    imgs_bytes = []
    zs = []
    image_pool = []
    path_of_the_directory= './input_images'
    for filename in os.listdir(path_of_the_directory):
        f = os.path.join(path_of_the_directory,filename)
        if os.path.isfile(f):
            image_pool.append(Image.open(f))
    amount = min(amount, 10)
    for i in range(amount):
        seed = np.random.randint(0,len(image_pool))
        image, z = image_pool[seed], seed
        imgs_bytes.append(Image_to_bytes(image))
        zs.append(z)
    
    sleep(1)
    return imgs_bytes, zs

def generate_transition(db, id1, id2, amount):
    img1 = search_by_id(db, id1)
    img2 = search_by_id(db, id2)
    imgs_bytes = [img1]
    zs = [0]
    img, zetas = generate_random_faces(amount - 1)
    for i,z in zip(img,zetas):
        imgs_bytes.append(i)
        imgs_bytes.append(z)
    imgs_bytes.append(img2)
    zs.append(0)
    sleep(3)
    return imgs_bytes, zs

def base64_to_latent(base64str):
    sleep(10)
    return base64str, 0

def change_features(db, id1, features_dict):
    img1 = search_by_id(db, id1)
    return img1, id1

def mix_styles(db, id1, id2):
    img1 = search_by_id(db, id1)
    img2 = search_by_id(db, id2)    
    return [img1, img2], [id1, id2]

def Image_to_bytes(img):
    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


def init_connection_pool_replica() -> sqlalchemy.engine.base.Engine:
    return connect_replica()

def search_by_id(db, id):
    stmt = sqlalchemy.text(
        "SELECT img from gen_images WHERE imgID = :id"
    )
    try:
        with db.connect() as conn:
            result = conn.execute(stmt, id=id)
            ans = result.fetchall()
            if len(ans) == 0:
                return None
            img_bytes = ans[0][0]
    except Exception as e:
        print(e)
        raise e
    return img_bytes