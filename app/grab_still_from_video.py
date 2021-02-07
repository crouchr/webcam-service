import integration_definitions


def grab_still_from_video(mp4_filename):
    """
    Grab first frame
    """
    import cv2

    jpeg_filename = mp4_filename.replace('mp4', 'jpg')

    vidcap = cv2.VideoCapture(mp4_filename)
    success, image = vidcap.read()
    cv2.imwrite(jpeg_filename, image)       # save frame as JPEG file

    return jpeg_filename


def main():
    mp4_filename = integration_definitions.MEDIA_ROOT + 'test_images/test_video.mp4'
    print('mp4_filename=' + mp4_filename)

    jpeg_filename = grab_still_from_video(mp4_filename)
    print('jpeg filename=' + jpeg_filename)


if __name__ == '__main__' :
    main()