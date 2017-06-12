import numpy as np
import keras.models
from keras.applications import VGG16,imagenet_utils
from keras.preprocessing.image import load_img,img_to_array
from flask import Flask, request, make_response,jsonify
import json
import urllib
import cv2
import os
from keras.models import model_from_json
import tensorflow as tf
app = Flask(__name__,static_url_path='')

model1=VGG16(include_top=False,weights='imagenet')
json_file=open('model.json','r')
loaded_model_json=json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("happy_sad.h5")
loaded_model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
vgg16_model=VGG16(include_top=False,weights='imagenet')

preprocess = imagenet_utils.preprocess_input

def load_im_from_url(url):
    requested_url = urllib.request.urlopen(url)
    image_array = np.asarray(bytearray(requested_url.read()), dtype=np.uint8)
    img = cv2.imdecode(image_array, -1)
    cv2.imwrite('test.png',img)

def predict(url):
    load_im_from_url(url)
    image = load_img('test.png',target_size=(224,224))
    image = img_to_array(image)
    image = np.expand_dims(image,axis=0)
    image = preprocess(image)
    feats = vgg16_model.predict(image)
    value = loaded_model.predict_proba(feats)
    return value

@app.route('/classify',methods=['GET'])
def classify():
    image_url=request.args.get('imageurl')
    value=predict(image_url)
    if value > 0.5:
        mood = 'Sad'
    else:
        mood = 'Happy'
    return jsonify({'results':mood})
@app.route('/',methods=['GET'])
def root():
    return app.send_static_file('index.html')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True,host='0.0.0.0',port=port,use_reloader=False)
