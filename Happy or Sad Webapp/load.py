import tensorflow as tf
from keras.models import model_from_json
import keras.models
def init():
    json_file=open('model.json','r')
    loaded_model_json=json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("happy_sad.h5")
    loaded_model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
    graph = tf.get_default_graph()
    return loaded_model,graph
