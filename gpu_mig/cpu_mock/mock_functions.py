from time import sleep
import base64
from io import BytesIO
import os
from PIL import Image
import numpy as np


def generate_random_faces(amount):
    sleep(1)
    # return predetermined images
    return Image_to_bytes()

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

def generate_transition(id1, id2, amount):
    sleep(1)
    # return predetermined images
    return Image_to_bytes()

def base64_to_latent(base64str):
    sleep(1)
    # return predetermined images
    return Image_to_bytes()

def change_features(id1, features_dict):
    sleep(1)
    # return predetermined images
    return Image_to_bytes()

def mix_styles(id1, id2):
    sleep(1)
    # return predetermined images
    return Image_to_bytes()

def Image_to_bytes(img):
    byte_arr = BytesIO()
    img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = base64.encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img
