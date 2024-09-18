import warnings
import json

import requests

from .models import *

warnings.filterwarnings("ignore", 'Unverified HTTPS request is being made to host')


class BaseApi:
	def __init__(self, base_url: str, api_key: str):
		self.base_url = base_url + ('/api' if '/api' not in base_url else '')
		self.api_key = api_key
		self.session = requests.Session()
		self.session.headers.update({'Content-Type': 'application/json'})
		self.session.headers.update({'Accept': 'application/json'})
		self.session.headers.update({'Authorization': f'Token {self.api_key}'})
		self.session.verify = False

	def _get(self, url: str, params: dict = None) -> dict:
		resp = self.session.get(self.base_url + url, params=params)
		resp.raise_for_status()
		return resp.json()

	def _post(self, url: str, params: dict = None, data: dict = None) -> dict:
		print(json.dumps(data))
		resp = self.session.post(self.base_url + url, params=params, json=data)
		resp.raise_for_status()
		return resp.json()

	def get_devices(self):
		return self._get('/dcim/devices')

	def get_device_types(self):
		return self._get('/dcim/device-types')

	def add_device_type(self, device_type: DeviceType):
		return self._post('/dcim/device-types', data=dict(device_type))

	def add_manufacturers(self, manufacturer: Manufacturer):
		return self._post('/dcim/manufacturers', data=dict(manufacturer))

	def get_manufacturers(self):
		return self._get('/dcim/manufacturers')
