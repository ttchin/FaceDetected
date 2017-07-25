# FaceDetected
A project based on tensor flow running on raspberry that can detect face.

## Requirements
1. Raspberrypi 3
2. Camera
3. Speaker
4. Python 3.5
5. Lots of images of the target and others
6. Put the images into data/target and others
  
## Prepare environments
### Prefer to train models on PC:
1. sudo apt-get install flint # for text to speech
2. conda install -c https://conda.anaconda.org/menpo opencv3
3. pip install requirements.txt

### Install on raspberry
1. For opencv:
http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
2. For Tensorflow:
https://github.com/samjabrahams/tensorflow-on-raspberry-pi
3. For keras:
https://github.com/bitschift/brew.ai/wiki/Setting-up-the-Pi
