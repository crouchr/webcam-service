import os


def get_version():
    if 'VERSION' in os.environ:
        version = os.environ['VERSION']
    else:
        version = 'IDE-1.0.0'   # i.e. running in PyCharm

    return version


# def get_video_length():
#     """
#     Set webcam video duration in Docker Compose ENV
#     """
#     if 'VIDEO_SECS' in os.environ:
#         video_length_secs = os.environ['VIDEO_SECS']
#     else:
#         video_length_secs = 5
#
#     return video_length_secs
#
#
# def get_video_preamble():
#     """
#     Set webcam video preamble duration in Docker Compose ENV
#     """
#     if 'PREAMBLE_SECS' in os.environ:
#         preamble_secs = os.environ['PREAMBLE_SECS']
#     else:
#         preamble_secs = 5
#
#     return preamble_secs
