import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout,Flatten,Dense
from keras import applications

## Defining our Hyper Parameters
img_width,img_height=224,224
model_weights_path='happy_sad.h5'
train_data_dir='data/train'
validation_data_dir='data/validation'
nb_train_samples = 256
nb_validation_samples = 20
epochs = 10
batch_size = 1
def generate_features():
    '''
    Parses the data folder and generates .npy file
    '''
    datagen=ImageDataGenerator(rescale=1./255.)
    model=applications.VGG16(include_top=False,weights='imagenet')
    generator = datagen.flow_from_directory(train_data_dir,
    target_size=(img_width,img_height),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)
    features_train=model.predict_generator(generator,nb_train_samples)
    np.save(open('features_train.npy','wb'),
    features_train)
    generator = datagen.flow_from_directory(validation_data_dir,
    target_size=(img_width,img_height),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)
    features_validation = model.predict_generator(generator,nb_validation_samples)
    np.save(open('features_validation.npy','wb'),
    features_validation)


if __name__ == '__main__':
    if not os.path.exists('./features_train.npy') and not os.path.exists('./features_validation.npy'):
        print ('Generating Features...')
        generate_features()
        print ('Features generated successfully!')
    train_data = np.load(open('features_train.npy','rb'))
    print(train_data[0].shape)
    train_labels=np.array([0] * 102 + [1] * 154)
    validation_data = np.load(open('features_validation.npy','rb'))
    #print (len(validation_data))
    validation_labels = np.array([0] * 10 + [1] * 10)
    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256,activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1,activation='sigmoid'))
    model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
    model.fit(train_data,train_labels,epochs=epochs,batch_size=batch_size,validation_data=(validation_data,validation_labels))
    score = model.evaluate(validation_data,validation_labels,verbose=0)
    print ('Validation loss:', score[0])
    print('Validation accuracy:',score[1])

    model_json=model.to_json()
    with open("model.json","w") as json_file:
        json_file.write(model_json)
    model.save_weights(model_weights_path)
    print("Saved model to disk")
