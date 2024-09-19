import warnings
import json

import requests
from loguru import logger

from .models import *

warnings.filterwarnings("ignore", 'Unverified HTTPS request is being made to host')


class BaseApi:
	def __init__(self, base_url: str, api_key: str, verify=True):
		self.base_url = base_url + ('/api' if '/api' not in base_url else '')
		self.session = requests.session()
		self.session.verify = verify
		self.session.headers.update({'accept': 'application/json'})
		self.session.headers.update({'Authorization': f'Token {api_key}'})

	def _get(self, url: str, params: dict = None) -> dict:
		logger.debug('GET ' + self.base_url + url + ' | ' + json.dumps(params))
		resp = self.session.get(self.base_url + url, params=params)
		return resp.json()

	def _post(self, url: str, params: dict = None, data: dict = None):
		logger.debug('POST ' + self.base_url + url + ' | ' + json.dumps(params) + ' | ' + json.dumps(data))
		resp = self.session.post(self.base_url + url, json=data, params=params)
		return resp.json()

	def get_devices(self):
		return self._get('/dcim/devices/')

	def get_device_types(self):
		return self._get('/dcim/device-types/')

	def add_device_type(self, device_type: DeviceType):
		return self._post('/dcim/device-types/', data=dict(device_type))

	def add_manufacturers(self, manufacturer: Manufacturer):
		return self._post('/dcim/manufacturers/', data=dict(manufacturer))

	def get_manufacturers(self):
		return self._get('/dcim/manufacturers/')

	def get_device_roles(self):
		return self._get('/dcim/device-roles/')

	def add_device_role(self, role: DeviceRole):
		return self._post('/dcim/device-roles/', data=dict(role))
