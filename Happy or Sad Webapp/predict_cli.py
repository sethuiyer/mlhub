import numpy as np
import keras.models
from keras.models import model_from_json
from keras.applications import VGG16,imagenet_utils
from keras.preprocessing.image import load_img,img_to_array
import argparse
preprocess=imagenet_utils.preprocess_input

parser = argparse.ArgumentParser(description='Enter the Image Path')
parser.add_argument('--image')
json_file=open('model.json','r')
loaded_model_json=json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("happy_sad.h5")
loaded_model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])


args = parser.parse_args()
image = load_img(args.image,target_size=(224,224))
image = img_to_array(image)
image = np.expand_dims(image,axis=0)
image = preprocess(image)
vgg16_model=VGG16(include_top=False,weights='imagenet')
feats = vgg16_model.predict(image)
value = loaded_model.predict_proba(feats)
if value >=0.5:
    print ('Predicted Mood: Sad')
else:
    print ('Predicted Mood: Happy')
