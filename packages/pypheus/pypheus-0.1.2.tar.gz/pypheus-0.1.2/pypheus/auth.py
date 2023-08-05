import requests
import json
import urllib3
urllib3.disable_warnings()

#
class Auth(object):

    def __init__(
            self, host,
            username, password):
        """
        Using oAuth to generate a token
        """
        self.username = username
        self.password = password
        self.host = host

        params = (
            ('grant_type', 'password'),
            ('scope', 'write'),
            ('client_id', 'morph-api'),
        )

        data = {
          'username': self.username,
          'password': self.password
        }

        url = 'http://' + self.host + '/oauth/token'

        response = requests.post(url, params=params, data=data)

        json_response = json.loads(response.text)

        access_token = json_response["access_token"]

        self.access_token = access_token
