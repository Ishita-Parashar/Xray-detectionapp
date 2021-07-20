import os
#os.chdir('D:\Data')
TrianImage="D:\\Data\\train\\"
TestImage="D:\\Data\\test\\"

#to get all image names in train file
p = os.listdir(TrianImage + "PNEUMONIA\\")
n = os.listdir(TrianImage + "NORMAL\\")
c = os.listdir(TrianImage + "COVID19\\")

import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.utils import np_utils
from keras.applications.resnet50 import preprocess_input


plt.figure(figsize = (12,12))
for i in range(4):
    plt.subplot(1, 4, i+1)
    img = plt.imread(os.path.join(TrianImage + "/PNEUMONIA",p[i]))
    plt.imshow(img)
    plt.title('PNEUMONIA : 1')
    plt.tight_layout()
plt.show()

plt.figure(figsize = (12,12))
for i in range(4):
    plt.subplot(1, 4, i+1)
    img = plt.imread(os.path.join(TrianImage + "/COVID19",c[i]))
    plt.imshow(img)
    plt.title("COVID19")
    plt.tight_layout()
plt.show()

plt.figure(figsize = (12,12))
for i in range(4):
    plt.subplot(1, 4, i+1)
    img = plt.imread(os.path.join(TrianImage + "/NORMAL",n[i]))
    plt.imshow(img)
    plt.title("NORMAL")
    plt.tight_layout()
plt.show()

from keras.preprocessing.image import ImageDataGenerator

train_datagen=ImageDataGenerator(rescale=1./255,shear_range=0.2,zoom_range=0.2,horizontal_flip=True)
test_datagen=ImageDataGenerator(rescale=1./255)

training_set=train_datagen.flow_from_directory(TrianImage,target_size=(224,224),batch_size=32,class_mode='categorical')

training_set.class_indices

test_set=test_datagen.flow_from_directory(TestImage,target_size=(224,224),
                                          batch_size=32,
                                          class_mode='categorical')

import keras
from keras.layers import Dense, Conv2D
from keras.layers import Flatten

from keras.layers import MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Activation
from keras.layers import BatchNormalization
from keras.layers import Dropout
from keras.models import Sequential
from keras import backend as K

from keras import optimizers

inputShape= (224,224,3)

model=Sequential()
model.add(Conv2D(32, (3,3), activation = 'relu', input_shape = inputShape))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization(axis =-1))
model.add(Dropout(0.2))

model.add(Conv2D(64, (3,3), activation = 'relu'))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization(axis = -1))
model.add(Dropout(0.2))

model.add(Conv2D(128, (3,3), activation = 'relu'))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization(axis = -1))

model.add(Dropout(0.2))

model.add(Conv2D(128, (3,3), activation = 'relu'))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization(axis = -1))

model.add(Dropout(0.2))

#model.add(Conv2D(128, (3,3), activation = 'relu'))
#model.add(MaxPooling2D(2,2))
#model.add(BatchNormalization(axis = -1))

#model.add(Dropout(0.2))


model.add(Flatten())

model.add(Dense(512, activation = 'relu'))
model.add(BatchNormalization(axis = -1))
model.add(Dropout(0.5))
model.add(Dense(3, activation = 'softmax'))

model.summary()

model.compile(loss = 'categorical_crossentropy', optimizer = 'Adam', metrics = ['accuracy'])

hist = model.fit_generator(
    training_set,
    epochs=1,
    #callbacks=[annealer,mc,es],
    steps_per_epoch=10,
    validation_data=test_set    
)

preds = model.evaluate(test_set)
print ("Validation Loss = " + str(preds[0]))
print ("Validation Accuracy = " + str(preds[1]))

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')
plt.show()

plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper right')
plt.show()

import numpy as np
predictions = np.argmax(model.predict(test_set), axis = -1)
predictions

from sklearn.metrics import classification_report, confusion_matrix
a=classification_report(test_set.classes,predictions)
print(a)

print(confusion_matrix(test_set.classes,predictions))
sns.heatmap(confusion_matrix(test_set.classes,predictions), annot = True)


def pred(image):
    image = keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis = 0)
    image = keras.applications.resnet50.preprocess_input(image)
    predictions = model.predict(image)
    prediction = list(training_set.class_indices)[np.argmax(predictions[0])]
    
    return prediction
#plt.imshow(image)
#pred(image)
#probabilities = model.predict_proba(image)


model.save("model.h5")



