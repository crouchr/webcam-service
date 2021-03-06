import uuid
import integration_definitions
import call_rest_api


def test_status():
    """
    Test /status
    :return:
    """

    query = {}
    this_uuid = uuid.uuid4()  # generate a uuid to simulate the client doing so
    query['app_name'] = 'integration_tests'
    query['uuid'] = this_uuid.__str__()

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.webcam_service_endpoint_base + '/status', query)

    if response_dict is None:
        return None

    assert status_code == 200
    assert response_dict['status'] == 'OK'
    assert 'version' in response_dict
    assert response_dict['uuid'] == this_uuid.__str__()