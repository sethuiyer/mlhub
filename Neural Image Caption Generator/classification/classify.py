from keras.applications import VGG16,imagenet_utils
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
import cv2
preprocess = imagenet_utils.preprocess_input

model = VGG16(weights="imagenet")
def convert_img_to_vector(img_path):
	image = load_img("img.jpg",target_size=(224,224))
	image = img_to_array(image)
	image = np.expand_dims(image,axis=0)
	image = preprocess(image)
	return image
def predict(img_vector):
	preds = model.predict(img_vector,verbose=0)
	P = imagenet_utils.decode_predictions(preds)
	return P[0][0][1]

prediction = predict(convert_img_to_vector("img.jpg"))
img = cv2.imread("img.jpg")
cv2.putText(img,"Label:{}".format(prediction),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
cv2.imwrite("img_output.jpg",img)
