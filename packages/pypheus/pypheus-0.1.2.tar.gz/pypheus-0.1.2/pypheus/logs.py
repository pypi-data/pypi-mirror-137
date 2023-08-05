#!/usr/bin/env python3
# coding=utf-8
# author: @netwookie
# -*- coding: utf-8 -*-
"""
Various storage API calls
"""
import urllib3
urllib3.disable_warnings()
from pypheus.auth import Auth
import json
import requests

class Logs(Auth):

    def __init__(
            self, host,
            username, password
            ):

        Auth.__init__(self, host, username, password)
        self.headers = {"Authorization": "BEARER " + self.access_token,'Accept': 'application/json'}
        self.endpoint ='https://' + host +  '/api'


    def get_all_logs(self, id=None):

    	if id:
    		id = str(id)
    		apps_url = self.endpoint + '/logs' + '/id'

    	else:

    		apps_url = self.endpoint + '/logs'

    	response = requests.get(apps_url, headers=self.headers,verify=False)

    	return response.json()
