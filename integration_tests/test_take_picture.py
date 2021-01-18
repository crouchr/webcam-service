import integration_definitions
import call_rest_api


def test_take_picture():
    """
    Test /status
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'
    #query['output_filename'] = '/tmp/junk.png'
    query['output_filename'] = '../images/junk.png'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.webcam_service_endpoint_base + '/get_image', query)

    if response_dict is None:
        assert False

    assert status_code == 200
    assert response_dict['status'] == 'OK'

