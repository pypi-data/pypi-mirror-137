#!/usr/bin/env python
import requests
from eureka import Eureka


class ApisClient(object):
    @staticmethod
    def get(service_name, endpoint):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.get(url).json()
        return response

    @staticmethod
    def post(service_name, endpoint, body=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.post(url, data=body)
        return response

    @staticmethod
    def put(service_name, endpoint, body=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.put(url, data=body)
        return response

    @staticmethod
    def delete(service_name, endpoint, body=None):
        url = Eureka.get_application_address(service_name) + endpoint
        response = requests.delete(url, data=body)
        return response


a = ApisClient().get('MAMMOTHMANAGER', '/api/v1/user/getCountries')
print(a)
