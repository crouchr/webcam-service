# microservice
import os
import time
import sys

from flask import Flask, jsonify, request

import get_version
import definitions
import webcam_capture

app = Flask(__name__)


# fixme : this does not give info about the actual exception
@app.errorhandler(500)
def error_handling(error):
    answer = {}
    answer['error'] = str(error)

    print('light_service() : error : ' + error.__str__())
    response = jsonify(answer, 500)

    return response


# an endpoint that can be polled with little overhead
@app.route('/status')
def status():
    answer = {}
    app_name = request.args.get('app_name')

    answer['status'] = 'OK'
    answer['version'] = get_version.get_version()

    print('status() : app_name=' + app_name.__str__() + ', version=' + answer['version'])
    response = jsonify(answer)

    return response


# @app.route('/stats')
# def stats():
#     answer = {}
#     app_name = request.args.get('app_name')
#
#     answer['status'] = 'OK'
#     answer['api_calls'] = -1    # not yet implemented
#
#     print('status() : app_name=' + app_name.__str__() + ', api_calls=' + answer['api_calls'])
#     response = jsonify(answer)
#
#     return response


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

        # code starts here
        output_filename = request.args.get('output_filename', None)     # name of output file

        print('get_image_api() : app_name=' + app_name.__str__() + ', output_filename=' + output_filename.__str__())

        webcam_capture.take_picture(output_filename)

        # Create response
        answer['status'] = 'OK'


        response = jsonify(answer)

        return response

    except Exception as e:
        answer['function'] = 'get_image_api()'
        answer['error'] = str(e)
        print('get_image_api() : app_name=' + app_name.__str__() + ', error : ' + e.__str__())
        response = jsonify(answer, 500)

        return response


if __name__ == '__main__':
    os.environ['PYTHONUNBUFFERED'] = "1"            # does this help with log buffering ?
    version = get_version() .get_version()          # container version

    print('webcam-service started, version=' + version)

    app.run(host='0.0.0.0', port=definitions.listen_port.__str__())
