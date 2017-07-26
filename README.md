# FaceDetected

A project based on tensor flow running on raspberry that can detect face.

## Requirements

1. Raspberrypi 3
1. Camera
1. Speaker
1. Python 3.5 on Windows/MacOs, Python 3.4 on Raspberry
1. ImageMagick <https://www.imagemagick.org/script/binary-releases.php>
1. Lots of images of the target and others
1. Put the images into data/target and others

## Prepare environments

### Prefer to train models on PC:

### In windows and macos, opencv only works on python 3.5

1. `conda create -n 3.5.2 python=3.5.2`
1. `conda install -c https://conda.anaconda.org/menpo opencv3`
1. `conda install h5py`
1. `conda install scipy`
1. `pip install keras`
1. `pip install sklearn`
1. `pip install tensorflow`

### Install on raspberry

### In raspberry, opencv only works on python 3.4**

1. For opencv:

<http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/>

1. For tensorflow:

<https://github.com/samjabrahams/tensorflow-on-raspberry-pi>

1. For keras:

<https://github.com/bitschift/brew.ai/wiki/Setting-up-the-Pi>

### Train models

1. Put your images
