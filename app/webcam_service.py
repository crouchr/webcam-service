# microservice
import os
import time
import sys

from flask import Flask, jsonify, request

import get_env
import definitions
import webcam_capture

app = Flask(__name__)


# fixme : this does not give info about the actual exception
@app.errorhandler(500)
def error_handling(error):
    answer = {}
    answer['error'] = str(error)

    print('webcam-service() : error : ' + error.__str__())
    response = jsonify(answer, 500)

    return response


# an endpoint that can be polled with little overhead
@app.route('/status')
def status():
    answer = {}
    app_name = request.args.get('app_name')
    this_uuid = request.args.get('uuid')

    answer['status'] = 'OK'
    answer['uuid'] = this_uuid.__str__()
    answer['service_name'] = 'webcam-service'
    answer['version'] = get_env.get_version()

    print('status() : app_name=' + app_name.__str__() + ', version=' + answer['version'])
    response = jsonify(answer)

    return response


@app.route('/get_image')
def get_image_api():
    """
    Retrieve an image from webcam
    :param app_name: e.g. name of the calling app so it can be identified in logs
    :return:
    """
    try:
        answer = {}
        app_name = request.args.get('app_name')
        this_uuid = request.args.get('uuid')

        # code starts here
        output_filename = request.args.get('output_filename', None)     # name of output file

        print('get_image_api() : app_name=' + app_name.__str__() + ', uuid=' + this_uuid.__str__() + ', output_filename=' + output_filename.__str__())

        if output_filename is None:
            output_filename = webcam_capture.create_media_filename(media_type='image')

        webcam_capture.take_picture(output_filename)

        # Create response
        answer['status'] = 'OK'
        answer['uuid'] = this_uuid
        answer['output_filename'] = output_filename
        answer['filesize'] = os.stat(output_filename).st_size          # Bytes

        response = jsonify(answer)

        return response

    except Exception as e:
        answer['function'] = 'get_image_api()'
        answer['error'] = str(e)
        print('get_image_api() : app_name=' + app_name.__str__() + ', error : ' + e.__str__())
        response = jsonify(answer, 500)

        return response


@app.route('/get_video')
def get_video_api():
    """
    Retrieve video from webcam
    :param app_name: e.g. name of the calling app so it can be identified in logs
    :return:
    """
    try:
        answer = {}
        app_name = request.args.get('app_name')
        this_uuid = request.args.get('uuid')
        video_length_secs = int(request.args.get('video_length_secs'))

        print('get_video_api() : app_name=' + app_name.__str__() + ', uuid=' + this_uuid.__str__())

        result, mp4_filename = webcam_capture.take_video(video_length_secs=video_length_secs)

        # Create response
        answer['status'] = 'OK'
        answer['uuid'] = this_uuid
        answer['output_filename'] = mp4_filename
        answer['filesize'] = os.stat(mp4_filename).st_size          # Bytes

        response = jsonify(answer)

        return response

    except Exception as e:
        answer['function'] = 'get_video_api()'
        answer['error'] = str(e)
        print('get_video_api() : app_name=' + app_name.__str__() + ', error : ' + e.__str__())
        response = jsonify(answer, 500)

        return response


if __name__ == '__main__':
    try:
        os.environ['PYTHONUNBUFFERED'] = "1"            # does this help with log buffering ?
        version = get_env.get_version()           # container version

        print('webcam-service started, version=' + version)

        app.run(host='0.0.0.0', port=definitions.webcam_service_listen_port.__str__())

    except Exception as e:
        print(e.__str__)
