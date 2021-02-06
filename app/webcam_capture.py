# POC
# take a picture of the sky so that the picture can be:
# a) sent in Forecast Tweet
# b) analysed to determine approximate light level
# c) analysed for cloud coverage

# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
# https://linuxconfig.org/how-to-install-mpeg-4-aac-decoder-for-centos-7-linux
# use smplayer for viewing


import time
import os
import traceback

import cv2

import video_compress_funcs
import definitions


def create_media_filename(media_type):
    """
    Generate a filename from the current time
    :return:
    """
    filename = "metminiwx_" + time.ctime()
    filename = filename.replace('  ', ' ')
    filename = filename.replace(' ', '_')
    filename = filename.replace(':', '_')

    if media_type == 'image':
        filename = filename + '.png'
    elif media_type == 'video':
        filename = filename + '.avi'

    full_pathname = definitions.MEDIA_ROOT + filename
    full_pathname = full_pathname.lower()

    return full_pathname


# can't get it to do anything except 640 x 480, 8-bit colour at the moment
def take_picture(image_filename):
    """
    Capture a png image
    """
    cam = cv2.VideoCapture(0)        # /dev/video0

    print('Grabbing still image from webcam...')
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab still image from webcam")
        return None

    cv2.imwrite(image_filename, frame)
    print("Image {} written to disk".format(image_filename))

    cam.release()

    time.sleep(1)

    return True


def take_video(video_length_secs, preamble_secs=0, crf=19, uuid=None):
    """
    Grab a video from webcam
    """
    try:
        fps = 30.0     # frames per second
        width = 640
        height = 480

        print('Grabbing ' + video_length_secs.__str__() + ' seconds of video from webcam, fps=' + fps.__str__() + ', uuid=' + uuid.__str__())
        video_filename = create_media_filename('video')     # name of the intermediate avi file

        cam = cv2.VideoCapture(0)                       # /dev/video0
        fourcc = cv2.VideoWriter_fourcc(*'XVID')        # .avi

        out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

        frames_captured = 0
        frames_to_capture = (preamble_secs + video_length_secs) * int(fps)
        frames_to_discard = preamble_secs * int(fps)     # cheap webcams are overexposed for first few seconds
        print('frames_to_capture=' + frames_to_capture.__str__())
        print('frames_to_discard=' + frames_to_discard.__str__())

        while cam.isOpened() and frames_captured < frames_to_capture:
            ret, frame = cam.read()
            if ret:
                if frames_captured > frames_to_discard:     # preamble period is over so not capture frames
                    out.write(frame)
                frames_captured += 1
            else:
                print('Error : Failed to grab video, uuid=' + uuid.__str__())
                break

        print('Video ' + video_filename + ' successfully written to disk, fps=' + fps.__str__() + ', uuid=' + uuid.__str__())

        cam.release()
        time.sleep(1)

        # convert avi to mp4/h264
        result, mp4_filename = video_compress_funcs.encode_to_mp4(video_filename, crf=crf, uuid=uuid)

        # remove the input avi file
        os.remove(video_filename)
        print('Deleted intermediate file ' + video_filename + ', uuid=' + uuid.__str__())

        if not result:  # failed
            return False, None
        else:           # video created OK
            return True, mp4_filename

    except Exception as e:
        traceback.print_exc()
        return False, None


if __name__ == '__main__':
    #print(cv2.__version__)
    #print(cv2.getBuildInformation())

    # media_filename = create_media_filename('image')
    # flag = take_picture('test_image.png')

    flag, mp4_filename = take_video(crf=10, video_length_secs=5)
