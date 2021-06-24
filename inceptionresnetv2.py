# -*- coding: utf-8 -*-
"""InceptionResNetV2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11NoUMSOXc9_mP9py_eFhsSoZDr1Uq5jB
"""

import keras


from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image
import numpy as np
import pandas as pd
#from tqdm import tqdm
from keras.layers import *

from keras.optimizers import *
from keras.applications import *
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
#from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import backend as k

#from keras.applications.inception_v3 import InceptionV3

#from keras.applications.vgg16 import VGG16

from keras.layers import Flatten,Dense,Dropout,BatchNormalization
from keras.models import Model,Sequential
from keras.utils import to_categorical
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization

#from keras.callbacks import ReduceLROnPlateau
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

train = pd.read_csv('/content/dataset/train.csv')    # reading the csv file


train_image = []
for i in range(train.shape[0]):
    img = image.load_img('/content/dataset/Train Images/'+train['Image'][i],target_size=(331,331,3))
    img = image.img_to_array(img)
    img = img/255
    
    train_image.append(img)
X = np.array(train_image)

import gc
del img
gc.collect()

import gc
del train_image
gc.collect()

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(train['Class'].astype(str))
train['Class'] = le.transform(train['Class'].astype(str))


y=train['Class'].values
y = to_categorical(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.3)

import gc
del X
gc.collect()


from keras.preprocessing.image import ImageDataGenerator
datagen = ImageDataGenerator()

pretrained_model = tf.keras.applications.InceptionResNetV2(input_shape=(331,331, 3), include_top=False,weights= 'imagenet')
for layer in pretrained_model.layers:
        layer.trainable = False

model = tf.keras.Sequential([
        pretrained_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        #tf.keras.layers.Dropout(0.5),
    
        #tf.keras.layers.Flatten(),
        #tf.keras.layers.Dense(1024, activation='relu'),
        

        tf.keras.layers.Dense(4, activation='softmax')
    ])




model.compile(
        optimizer='nadam',
        loss = 'categorical_crossentropy',
        metrics=['accuracy'])

batch_size = 16
model.fit_generator(
    datagen.flow(X_train, y_train, batch_size=batch_size),
    steps_per_epoch= X_train.shape[0] // batch_size,
    epochs=10,
    validation_data=(X_test, y_test),validation_steps = X_test.shape[0] // batch_size
    
    
    )

test = pd.read_csv('/content/dataset/test.csv')    # reading the csv file

test_image = []
for i in range(test.shape[0]):
    img = image.load_img('/content/dataset/Test Images/'+test['Image'][i],target_size=(331,331,3))
    img = image.img_to_array(img)
    img = img/255
    test_image.append(img)
test = np.array(test_image)

import gc
del img
gc.collect()

import gc
del test_image
gc.collect()

prediction = model.predict_classes(test)
predictions = le.inverse_transform(prediction)


sample = pd.read_csv('/content/dataset/test.csv')
sample['Class'] = predictions
sample.to_csv('New.csv', header=True, index=False)



