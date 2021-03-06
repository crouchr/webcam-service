import uuid
import integration_definitions
import call_rest_api


def test_take_picture():
    """
    Test /status
    :return:
    """
    query = {}
    this_uuid = uuid.uuid4()  # generate a uuid to simulate the client doing so

    query['app_name'] = 'integration_tests'
    query['uuid'] = this_uuid.__str__()

    query['output_filename'] = integration_definitions.MEDIA_ROOT + 'test_images/integration_test_image.png'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.webcam_service_endpoint_base + '/get_image', query)

    if response_dict is None:
        assert False

    assert status_code == 200
    assert response_dict['status'] == 'OK'
    assert response_dict['uuid'] == this_uuid.__str__()
    assert int(response_dict['filesize']) > 0