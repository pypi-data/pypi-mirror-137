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

class Monitoring(Auth):

    def __init__(
            self, host,
            username, password
            ):

        Auth.__init__(self, host, username, password)
        self.headers = {"Authorization": "BEARER " + self.access_token,'Accept': 'application/json'}
        self.endpoint ='https://' + host +  '/api'


    def get_all_checks(self, id=None):

    	if id:
    		id = str(id)
    		apps_url = self.endpoint + '/checks' + '/id'

    	else:

    		apps_url = self.endpoint + '/checks'

    	response = requests.get(apps_url, headers=self.headers,verify=False)

    	return response.json()

    def get_all_incidents(self, id=None):

    	if id:
    		id = str(id)
    		apps_url = self.endpoint + '/incidents' + '/id'

    	else:

    		apps_url = self.endpoint + '/incidents'

    	response = requests.get(apps_url, headers=self.headers,verify=False)

    	return response.json()

    def get_all_alerts(self, id=None):

        if id:
            id = str(id)
            apps_url = self.endpoint + '/alerts' + '/id'

        else:

            apps_url = self.endpoint + '/alerts'

        response = requests.get(apps_url, headers=self.headers,verify=False)

        return response.json()

    def get_all_contacts(self, id=None):

        if id:
            id = str(id)
            apps_url = self.endpoint + '/contacts' + '/id'

        else:

            apps_url = self.endpoint + '/contacts'

        response = requests.get(apps_url, headers=self.headers,verify=False)

        return response.json()
