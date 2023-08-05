#!/usr/bin/env python3
# coding=utf-8
# author: @netwookie
# -*- coding: utf-8 -*-
"""
Various network API calls
"""
import urllib3
urllib3.disable_warnings()
from pypheus.auth import Auth
import json
import requests

class Network(Auth):

    def __init__(
            self, host,
            username, password
            ):

        Auth.__init__(self, host, username, password)
        self.headers = {"Authorization": "BEARER " + self.access_token,'Accept': 'application/json'}
        self.endpoint ='https://' + host +  '/api'


    def get_all_networks(self, id=None):

    	if id:
    		id = str(id)
    		apps_url = self.endpoint + '/networks' + '/id'

    	else:

    		apps_url = self.endpoint + '/networks'

    	response = requests.get(apps_url, headers=self.headers,verify=False)

    	return response.json()

    def network_types(self, id=None):

    	if id:
    		id = str(id)
    		apps_url = self.endpoint + '/network-types' + '/id'

    	else:

    		apps_url = self.endpoint + '/network-types'

    	response = requests.get(apps_url, headers=self.headers,verify=False)

    	return response.json()

    def network_routers(self, id=None):

        if id:
            id = str(id)
            apps_url = self.endpoint + '/networks/routers' + '/id'

        else:

            apps_url = self.endpoint + '/networks/routers'

        response = requests.get(apps_url, headers=self.headers,verify=False)

        return response.json()
