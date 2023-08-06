import requests
from jsonschema import validate

def get_api(endpoint, header):
    """please pass headers as {} if no headers"""
    response = requests.get(url=endpoint, headers=header, verify=False)
    return response


def post_api(endpoint, request_payload, header):
    response = requests.post(url=endpoint, data=request_payload, headers=header)
    return response


def put_api(endpoint, request_payload, header):
    response = requests.post(url=endpoint, data=request_payload, headers=header)
    return response


def delete_api(endpoint, data, header):
    response = requests.delete(url=endpoint, params=data, headers=header)
    return response


def validate_status_code(response, expected_status):
    assert response.status_code is int(expected_status)


def validate_schema(response, expected_schema):
    validate(instance=response, schema=expected_schema)
    
