#! encoding: UTF-8

from __future__ import print_function
import random

import numpy as np
from sklearn.cross_validation import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.models import load_model
from keras import backend as K

from FaceInput import extract_data, resize_with_pad, IMAGE_SIZE
import os

class Dataset(object):

    def __init__(self):
        self.X_train = None
        self.X_valid = None
        self.X_test = None
        self.Y_train = None
        self.Y_valid = None
        self.Y_test = None

    def read(self, nb_classes, img_rows=IMAGE_SIZE, img_cols=IMAGE_SIZE, img_channels=3):
        images, labels = extract_data('./train/')
        labels = np.reshape(labels, [-1])
        # numpy.reshape
        X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, random_state=random.randint(0, 100))
        X_valid, X_test, y_valid, y_test = train_test_split(images, labels, test_size=0.5, random_state=random.randint(0, 100))
        
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 3)
        X_valid = X_valid.reshape(X_valid.shape[0], img_rows, img_cols, 3)
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 3)
        input_shape = (img_rows, img_cols, 3)

        # the data, shuffled and split between train and test sets
        print('X_train shape:', X_train.shape)
        print(X_train.shape[0], 'train samples')
        print(X_valid.shape[0], 'valid samples')
        print(X_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        Y_train = np_utils.to_categorical(y_train, nb_classes)
        Y_valid = np_utils.to_categorical(y_valid, nb_classes)
        Y_test = np_utils.to_categorical(y_test, nb_classes)

        X_train = X_train.astype('float32')
        X_valid = X_valid.astype('float32')
        X_test = X_test.astype('float32')
        X_train /= 255
        X_valid /= 255
        X_test /= 255

        self.X_train = X_train
        self.X_valid = X_valid
        self.X_test = X_test
        self.Y_train = Y_train
        self.Y_valid = Y_valid
        self.Y_test = Y_test


class Model(object):

    FILE_PATH = './model/model.h5'

    def __init__(self):
        self.model = None

    def build_model(self, dataset, nb_classes):
        self.model = Sequential()
        self.dataset = dataset
        self.model.add(
            Convolution2D(
                filters=32,
                kernel_size=(5, 5),
                padding='same',
                dim_ordering='tf',
                input_shape=self.dataset.X_train.shape[1:]
            )
        )

        self.model.add(Activation('relu'))
        self.model.add(
            MaxPooling2D(
                pool_size=(2, 2),
                strides=(2, 2),
                padding='same'
            )
        )
        

        self.model.add(Convolution2D(filters=64, kernel_size=(5, 5), padding='same'))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
        

        self.model.add(Flatten())
        self.model.add(Dense(512))
        self.model.add(Activation('relu'))
        

        self.model.add(Dense(nb_classes))
        self.model.add(Activation('softmax'))
        self.model.summary()

    def train(self, dataset, batch_size=20, nb_epoch=7, data_augmentation=True):
        self.model.compile(
            optimizer='adam',  #有很多可选的optimizer，例如RMSprop,Adagrad，你也可以试试哪个好，我个人感觉差异不大
            loss='categorical_crossentropy',  #你可以选用squared_hinge作为loss看看哪个好
            metrics=['accuracy'])

        if not data_augmentation:
            print('Not using data augmentation.')
            self.model.fit(dataset.X_train, dataset.Y_train,
                           batch_size=batch_size,
                           nb_epoch=nb_epoch,
                           validation_data=(dataset.X_valid, dataset.Y_valid),
                           shuffle=True)
            #epochs、batch_size为可调的参数，epochs为训练多少轮、batch_size为每次训练多少个样本
            #self.model.fit(self.dataset.X_train,self.dataset.Y_train,nb_epoch,batch_size)
        else:
            print('Using real-time data augmentation.')

            # this will do preprocessing and realtime data augmentation
            datagen = ImageDataGenerator(
                featurewise_center=False,             # set input mean to 0 over the dataset
                samplewise_center=False,              # set each sample mean to 0
                featurewise_std_normalization=False,  # divide inputs by std of the dataset
                samplewise_std_normalization=False,   # divide each input by its std
                zca_whitening=False,                  # apply ZCA whitening
                rotation_range=20,                     # randomly rotate images in the range (degrees, 0 to 180)
                width_shift_range=0.2,                # randomly shift images horizontally (fraction of total width)
                height_shift_range=0.2,               # randomly shift images vertically (fraction of total height)
                horizontal_flip=True,                 # randomly flip images
                vertical_flip=False)                  # randomly flip images

            # compute quantities required for featurewise normalization
            # (std, mean, and principal components if ZCA whitening is applied)
            datagen.fit(dataset.X_train)

            # fit the model on the batches generated by datagen.flow()
            self.model.fit_generator(datagen.flow(dataset.X_train, dataset.Y_train,
                                                  batch_size=batch_size),
                                     samples_per_epoch=dataset.X_train.shape[0],
                                     nb_epoch=nb_epoch,
                                     validation_data=(dataset.X_valid, dataset.Y_valid))
        

    def save(self, file_path=FILE_PATH):
        print('Model Saved.')
        self.model.save(file_path)

    def load(self, file_path=FILE_PATH):
        print('Model Loaded.')
        self.model = load_model(file_path)

    def predict(self, image):
        if K.image_dim_ordering() == 'tf' and image.shape != (1, IMAGE_SIZE, IMAGE_SIZE, 3):
            image = resize_with_pad(image)
            image = image.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 3))
        image = image.astype('float32')
        image /= 255
        result = self.model.predict_proba(image)
        print(result)
        max_index = np.argmax(result)

        return max_index,result[0][max_index]

    def evaluate(self, dataset):
        score = self.model.evaluate(dataset.X_test, dataset.Y_test, verbose=0)
        print("%s: %.2f%%" % (self.model.metrics_names[1], score[1] * 100))

    def getTrainCfg(self):
        array=[]
        with open("./model/train.cfg", 'r') as fread:
            lines = fread.readlines()
            for name in lines:
                array.append(name.strip("\n"))
        print(array)
        return enumerate(array)

    def generateTrainCfg(self):
        with open("./model/train.cfg", "w+") as fwrite:
            for dir in os.listdir("train"):
                if not dir.startswith("."):  # avoid hidden folder like .DS_Store
                    fwrite.write("{}\n".format(dir))

if __name__ == '__main__':
    count = 0
    for dir in os.listdir("train"):
        count +=1
    print("%d type objects need to be trained" % count)

    dataset = Dataset()
    dataset.read(count)

    model = Model()
    model.build_model(dataset,count)
    model.train(dataset, data_augmentation=False)
    model.save()

    model = Model()
    model.load()
    model.evaluate(dataset)
    model.generateTrainCfg()
