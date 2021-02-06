# Infinite loop for grabbing sky videos and posting to Twitter if there is sufficient light
# TODO : only tweet if other weather conditions are interesting e.g. wind ? minimum
# This is basically a script showing how to use the various microservices

import time
import uuid

import call_rest_api
import integration_definitions


def get_lux():
    """
    Read lux/watts levels from light sensor
    """
    query = {}                                  # API call to light-service
    query['app_name'] = 'take_sky_webcamd'
    light_service_listen_port = 9503
    light_service_endpoint_base = 'http://192.168.1.180:' + light_service_listen_port.__str__()
    status_code, response_dict = call_rest_api.call_rest_api(light_service_endpoint_base + '/get_lux', query)
    lux = response_dict['lux']
    sky_condition = response_dict['sky_condition']
    watts = response_dict['watts']

    return int(lux), int(watts), sky_condition


def send_tweet(tweet_text, filename, uuid):
    """
    Send a Tweet with a video file
    """
    query = {}                                  #API call to twitter-service
    query['app_name'] = 'take_sky_webcamd'
    query['uuid'] = uuid
    query['tweet_text'] = tweet_text
    query['hashtag_arg'] = 'testing'    # do not supply the #
    query['lat'] = 51.4151              # Stockcross
    query['lon'] = -1.3776              # Stockcross
    query['video_pathname'] = filename

    twitter_service_endpoint_base = 'http://192.168.1.5:9506'
    status_code, response_dict = call_rest_api.call_rest_api(twitter_service_endpoint_base + '/send_video', query)


def main():

    min_lux = 5                     # was 100
    crf = 19                        # H264 encoding quality parameter
    my_app_name = 'take_sky_webcamd'
    video_length_secs = 20           # 20

    webcam_query = {}               # API call to webcam-service
    webcam_query['app_name'] = my_app_name
    webcam_query['video_length_secs'] = video_length_secs
    webcam_query['preamble_secs'] = 5

    print('take_sky_webcamd : started...')

    while True:
        this_uuid = uuid.uuid4().__str__()          # unique uuid per cycle

        lux, watts, sky_condition = get_lux()
        if lux <= min_lux:                  # do not bother taking video if it is too dark
            print(time.ctime() + ' : light level is below ' + min_lux.__str__() + ' lux, so sleeping... lux=' + lux.__str__())
            time.sleep(600)                 # 10 minutes
            continue

        webcam_query['uuid'] = this_uuid
        print('Grabbing webcam video... uuid=' + this_uuid)
        status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.webcam_service_endpoint_base + '/get_video', webcam_query)
        mp4_filename = response_dict['output_filename']

        print('wrote webcam video to : ' + mp4_filename)

        filename = mp4_filename.split('/')[-1]      # ignore the filepath

        # Tweet the video
        tweet_text = 'take_sky_webcamd, lux=' + lux.__str__() + \
            ', watts=' + watts.__str__() + \
            ', condition=' + sky_condition + \
            ', crf=' + crf.__str__() + \
            ', file=' + filename

        send_tweet(tweet_text, mp4_filename, this_uuid)

        mins_between_videos = 15
        sleep_secs = mins_between_videos * 60
        print('----------------------------------------------')
        print(time.ctime() + ' sleeping for ' + sleep_secs.__str__() + ' ...')
        time.sleep(sleep_secs)


if __name__ == '__main__':
    main()
