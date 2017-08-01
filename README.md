# FaceDetected

A project based on tensor flow running on Raspberry that can detect face.

## Requirements

1. Raspberrypi 3
1. Camera
1. Speaker
1. Python 3.5 on Windows/MacOs, Python 3.4 on Raspberry
1. Lots of images of the target and others
1. Put the images into data/target and others

## Prepare environments

### In windows and macos, opencv only works on python 3.5

1. `conda create -n 3.5.2 python=3.5.2`
1. `source activate 3.5.2` for Linux/MacOS or `activate 3.5.2` for Windows
1. `conda install -c https://conda.anaconda.org/menpo opencv3`
1. `conda install h5py`
1. `conda install scipy`
1. `pip install keras`
1. `pip install sklearn`
1. `pip install pygame`
1. `pip install tensorflow`

### In raspberry, opencv only works on python 3.4**

1. For opencv:<http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/>

1. For tensorflow:<https://github.com/samjabrahams/tensorflow-on-raspberry-pi>

1. For keras:<https://github.com/bitschift/brew.ai/wiki/Setting-up-the-Pi>

## Prepare images

### Capture pictures and crop faces from the camera video stream

* e.g. `python CapturePictures.py -n 50`
* `python CapturePictures.py -h` will give you more information.

### Or crop faces from the existing pictures

* e.g. `python CropFaces.py -d ./captured_pictures/`
* `python CropFaces.py -h` will give you more information.

## Train models

1. Put your cropped images and the other's images into train/boss and train/other respectively.
1. `python FaceTrain.py` will generate a model into ./model

## Start face detected

When the model is ready, `python FaceDeted.py` will capture a picture from the camera and identify if it's you or not.
