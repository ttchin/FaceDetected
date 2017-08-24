#%%
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras import backend as K
from keras.models import Sequential
from keras.models import Model as M
from keras.layers import Conv2D,Convolution2D, MaxPooling2D
from FaceTrain import Model
from FaceInput import extract_data, resize_with_pad, IMAGE_SIZE


def visualizeLayer(pic):
    pic = resize_with_pad(pic)
    batch = np.expand_dims(pic, axis=0)
    batch = batch.astype('float32')
    batch /= 255
    print("resize shape: {}".format(batch.shape))

    model = Sequential()
    
    model.add(
        Convolution2D(
            filters=32,
            kernel_size=(3, 3),
            padding='same',
            dim_ordering='tf',
            input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
            name="1"
        )
    )

    model.add(Activation('relu',name="2"))
    model.add(
        MaxPooling2D(
            pool_size=(2, 2),
            strides=(2, 2),
            padding='same',
            name="3"
        )
    )

    model.add(Flatten(name='7'))
    model.add(Dense(512,name="8"))
    model.add(Activation('relu',name='9'))

    model.add(Dense(2,name='10'))
    model.add(Activation('softmax',name='11'))
    model.summary()

    for layer in model.layers:
        layerName = layer.get_config().get('name')
        print("Output layer : {}".format(layerName))
        intermediate_layer_model = M(inputs=model.input,
                                        outputs=model.get_layer(layerName).output)
        intermediate_output = intermediate_layer_model.predict(batch)
        layer_output = intermediate_output

        print("layer_output: {}".format(layer_output.shape))
        
        if(len(layer_output.shape) == 4):
            pic = np.squeeze(layer_output, axis=0)
            print("shape after squeeze: {}".format(pic[:,:,0].shape))
            pic_no = pic.shape[2]
            for i in range(pic_no):
                output_img = pic[:,:,i]
                output_img *=255
                cv2.imwrite('./temp/{}_{}.bmp'.format(layerName,i), output_img)


if __name__ == '__main__':
    pic = cv2.imread('./temp/original.jpg')
    # plt.imshow(pic)
    print("original shape: {}".format(pic.shape))
    visualizeLayer(pic)