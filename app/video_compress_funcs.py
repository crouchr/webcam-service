import os

# import mytwython
import webcam_capture

# less verbose output ffmpeg -hide_banner -loglevel panic
# https://superuser.com/questions/525249/convert-avi-xvid-to-mp4-h-264-keeping-the-same-quality
# ffmpeg -i input.avi -c:v libx264 -crf 19 -preset slow -c:a libfdk_aac -b:a 192k -ac 2 out.mp4
# -an : disable audio
# -y : allow overwrite outputfile
# crf controls quality lower crf = better quality crf=19 is a good starting point
def encode_to_mp4(input_avi_filename, crf=19, uuid=None):
    """
    Encode to MP4 H.264 which is Twitter's video format
    :param input_avi_filename:
    :return:
    """

    output_mp4_filename = input_avi_filename.split('.')[0] + '.mp4'
    print('encode_to_mp4() : encoding ' + input_avi_filename + ' video to MP4/H264, crf=' + crf.__str__() + ', uuid=' + uuid.__str__())
    # cmd_str = 'ffmpeg -i ' + input_avi_filename + ' -an -y -c:v libx264 -crf 19 -preset slow -c:a libfdk_aac -b:a 192k -ac 2 ' + output_mp4_filename
    cmd_str = 'ffmpeg -i ' + input_avi_filename + ' -loglevel quiet -stats -an -y -c:v libx264 -crf ' + crf.__str__() + ' -preset slow -c:a libfdk_aac -b:a 192k -ac 2 ' + output_mp4_filename
    print(cmd_str)
    result = os.system(cmd_str)     # can't tell if it ran OK

    if not os.path.exists(input_avi_filename):
        print('Error : input file ' + input_avi_filename + ' does not exist, uuid=' + uuid.__str__())
    else:
        file_stats = os.stat(input_avi_filename)
        input_file_size = round(file_stats.st_size / (1024 * 1024), 2)
        print('input video file : ' + input_avi_filename + ', AVI size (MB) : ' + input_file_size.__str__())

    if not os.path.exists(output_mp4_filename):
        print('Error : output file ' + output_mp4_filename + ' does not exist, uuid=' + uuid.__str__())
        result = False
    else:
        file_stats = os.stat(output_mp4_filename)
        output_file_size = round(file_stats.st_size / (1024 * 1024), 2)
        print('output video file created OK : ' + output_mp4_filename + ', MP4 size (MB) : ' + output_file_size.__str__() + ', uuid=' + uuid.__str__())
        result = True

    return result, output_mp4_filename


# test harness
if __name__ == '__main__':

    media_filename = 'sky.avi'
    # get webcam avi video
    flag, mp4_filename = webcam_capture.take_video(media_filename, video_length_secs=20, crf=10)

    # convert avi to MP4
    # mp4_filename = encode_to_mp4('sky.avi', crf=10)

    # Test that Twitter will accept it
    tweet_text = 'testing from video_compress_funcs'
    # mytwython.send_tweet(tweet_text, hashtags=None, media_type='video', media_pathname=mp4_filename)
