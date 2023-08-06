# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import json
import os
import unittest
from lupuxt2py import LupusecSevice
from urllib3_mock import Responses

responses = Responses('requests.packages.urllib3')

def get_env_data_as_dict(path: str) -> dict:
    if not os.path.isfile(path):
        return {"host":"","password":"","user":""}
    with open(path, 'r') as f:
        return dict(tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#'))


data = get_env_data_as_dict("../.env")

# get parent directory
dir=os.path.join(os.path.dirname(__file__))

class TestLupusec(unittest.TestCase):


    @responses.activate
    def test_get_sensors(self):
        responses.add('GET', '/action/tokenGet',
                      body='{"message": "123"}', status=404,
                      content_type='application/json')
        lupusec = LupusecSevice(ip_address="localhost:1080",
                                username=data["user"],
                                password=data["password"])
        with open(dir+'/response.json') as f:
            contents = f.read()
            responses.add('GET', '/action/deviceGet',
                          body=contents, status=200,
                          content_type='application/json')
        flatten = [val for sublist in lupusec.get_sensor_list().values() for val in sublist]
        self.assertEqual(flatten.__len__(), 54)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
