#! encoding: UTF-8

import os

import cv2
import cv

videos_src_path = '../videos'
videos_save_path = '../before'

videos = os.listdir(videos_src_path)
videos = filter(lambda x: x.endswith('h264'), videos)

for each_video in videos:
    print each_video

    # get the name of each video, and make the directory to save frames
    each_video_name, _ = each_video.split('.')
    os.mkdir(videos_save_path + '/' + each_video_name)               

    each_video_save_full_path = os.path.join(videos_save_path, each_video_name) + '/'

    # get the full path of each video, which will open the video tp extract frames
    each_video_full_path = os.path.join(videos_src_path, each_video)

    cap  = cv2.VideoCapture(each_video_full_path)
    frame_count = 1
    success = True
    while(success):
        success, frame = cap.read()
        print 'Read a new frame: ', success

        params = []
        params.append(cv.CV_IMWRITE_PXM_BINARY)
        params.append(1)
        cv2.imwrite(each_video_save_full_path + each_video_name + "_%d.jpg" % frame_count, frame, params)

        frame_count = frame_count + 1

cap.release()