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

    model = Model()
    model.load()
    # print(model.model.layers)
    for layer in model.model.layers:
        layerName = layer.get_config().get('name')
        print("Output layer : {}".format(layerName))
        intermediate_layer_model = M(inputs=model.model.input,
                                        outputs=model.model.get_layer(layerName).output)
        intermediate_output = intermediate_layer_model.predict(batch)
        layer_output = intermediate_output

        print("layer_output: {}".format(layer_output.shape))
        
        if(len(layer_output.shape) == 4):
            pic = np.squeeze(layer_output, axis=0)
            print("shape after squeeze: {}".format(pic[:,:,0].shape))
            pic_no = pic.shape[2]
            for i in range(pic_no):
                # print(i)
                output_img = pic[:,:,i]
                output_img *=255
                # print(output_img)
                # plt.imshow(output_img)
                cv2.imwrite('./temp/{}_{}.jpg'.format(layerName,i), output_img)


if __name__ == '__main__':
    pic = cv2.imread('./temp/original.jpg')
    plt.imshow(pic)
    print("original shape: {}".format(pic.shape))
    visualizeLayer(pic)