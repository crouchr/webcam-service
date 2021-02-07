# Infinite loop for grabbing sky videos and posting to Twitter if there is sufficient light
# TODO : only tweet if other weather conditions are interesting e.g. wind ? minimum
# This is basically a script showing how to use the various microservices

import time
import uuid

import call_rest_api
import integration_definitions
import get_env
import get_cumulus_weather_info


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
    query = {}                                  # API call to twitter-service
    query['app_name'] = 'take_sky_webcamd'
    query['uuid'] = uuid
    query['tweet_text'] = tweet_text
    query['hashtag_arg'] = 'metminiwx'          # do not supply the #
    query['lat'] = 51.4151                      # Stockcross
    query['lon'] = -1.3776                      # Stockcross
    query['video_pathname'] = filename

    twitter_service_endpoint_base = 'http://192.168.1.5:9506'
    status_code, response_dict = call_rest_api.call_rest_api(twitter_service_endpoint_base + '/send_video', query)


def main():

    min_lux = 100                           # was 100
    crf = 19                                # H264 encoding quality parameter
    my_app_name = 'take_sky_webcamd'

    video_length_secs = 20                  # use 5 for testing
    preamble_secs = 5

    webcam_query = {}                       # API call to webcam-service
    webcam_query['app_name'] = my_app_name
    webcam_query['video_length_secs'] = video_length_secs
    webcam_query['preamble_secs'] = preamble_secs

    print('take_sky_webcamd : started...')

    while True:
        this_uuid = uuid.uuid4().__str__()          # unique uuid per cycle

        cumulus_weather_info = get_cumulus_weather_info.get_key_weather_variables()     # REST API call

        lux, watts, sky_condition = get_lux()
        if lux <= min_lux:                  # do not bother taking video if it is too dark
            print(time.ctime() + ' : light level is below ' + min_lux.__str__() + ' lux, so sleeping... lux=' + lux.__str__())
            time.sleep(600)                 # 10 minutes
            continue

        webcam_query['uuid'] = this_uuid
        print('Grabbing webcam mp4 video and a jpg..., uuid=' + this_uuid)
        status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.webcam_service_endpoint_base + '/get_video', webcam_query)
        mp4_filename = response_dict['video_filename']
        jpeg_filename = response_dict['jpeg_filename']

        print('wrote webcam video to : ' + mp4_filename + ', uuid=' + this_uuid)
        print('wrote webcam jpeg to  : ' + jpeg_filename + ', uuid=' + this_uuid)

        filename = mp4_filename.split('/')[-1]      # ignore the filepath

        # Tweet the video
        tweet_text = 'take_sky_webcamd :' +\
            ' ' + cumulus_weather_info['Beaufort'] + ' max=' + cumulus_weather_info['HighBeaufortToday'] + \
            ', cbase=' + cumulus_weather_info['Cloudbase'].__str__() + ' ' + cumulus_weather_info['CloudbaseUnit'] + \
            ', ' + cumulus_weather_info['Pressure'].__str__() + ' ' + cumulus_weather_info['PressUnit'] + \
            ', trend=' + cumulus_weather_info['PressTrend'].__str__() + \
            ', temp=' + cumulus_weather_info['OutdoorTemp'].__str__() + cumulus_weather_info['TempUnit'] + \
            ', wind_chill=' + cumulus_weather_info['WindChill'].__str__() + cumulus_weather_info['TempUnit'] + \
            ', dew_point=' + cumulus_weather_info['OutdoorDewpoint'].__str__() + cumulus_weather_info['TempUnit'] + \
            ', ' + cumulus_weather_info['DominantWindDirection'] + \
            ', last_rain=' + cumulus_weather_info['LastRainTipISO'] + \
            ', fcast=' + cumulus_weather_info['Forecast'] + \
            ', watts=' + watts.__str__() + \
            ', lux=' + lux.__str__() + \
            ', sunrise=' + cumulus_weather_info['Sunrise'] + \
            ', sunset=' + cumulus_weather_info['Sunset'] + \
            ' ' + filename

        send_tweet(tweet_text, mp4_filename, this_uuid)
        print(tweet_text)

        mins_between_videos = 15
        sleep_secs = mins_between_videos * 60
        print('----------------------------------------------')
        print(time.ctime() + ' sleeping for ' + sleep_secs.__str__() + ' ...')
        time.sleep(sleep_secs)


if __name__ == '__main__':
    main()
