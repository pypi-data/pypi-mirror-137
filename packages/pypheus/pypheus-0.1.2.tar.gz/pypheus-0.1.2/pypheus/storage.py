#!/usr/bin/env python3
# coding=utf-8
# author: @netwookie.
# -*- coding: utf-8 -*-
"""
Various storage API calls
"""
import urllib3
urllib3.disable_warnings()
from pypheus.auth import Auth
import json
import requests

class Storage(Auth):

    def __init__(
            self, host,
            username, password
            ):

        Auth.__init__(self, host, username, password)
        self.headers = {"Authorization": "BEARER " + self.access_token,'Accept': 'application/json'}
        self.endpoint ='https://' + host +  '/api'


    def get_all_volumes(self, id=None):

    	if id:
    		id = str(id)
    		apps_url = self.endpoint + '/storage-volumes' + '/id'

    	else:

    		apps_url = self.endpoint + '/storage-volumes'

    	response = requests.get(apps_url, headers=self.headers,verify=False)

    	return response.json()

    def get_all_buckets(self, id=None):

    	if id:
    		id = str(id)
    		apps_url = self.endpoint + '/storage-buckets' + '/id'

    	else:

    		apps_url = self.endpoint + '/storage-buckets'

    	response = requests.get(apps_url, headers=self.headers,verify=False)

    	return response.json()

    def get_all_servers(self, id=None):

        if id:
            id = str(id)
            apps_url = self.endpoint + '/storage-servers' + '/id'

        else:

            apps_url = self.endpoint + '/storage-servers'

        response = requests.get(apps_url, headers=self.headers,verify=False)

        return response.json()

    def get_all_server_types(self, id=None):

        if id:
            id = str(id)
            apps_url = self.endpoint + '/storage-server-types' + '/id'

        else:

            apps_url = self.endpoint + '/storage-server-types'

        response = requests.get(apps_url, headers=self.headers,verify=False)

        return response.json()
