import warnings
import json

import requests
from loguru import logger

from .models import *
from .API_Module import IPAM, DCIM, Wireless

warnings.filterwarnings("ignore", 'Unverified HTTPS request is being made to host')


class BaseApi(IPAM, DCIM, Wireless):
	def __init__(self, base_url: str, api_key: str, verify=True):
		self.base_url = base_url + ('/api' if '/api' not in base_url else '')
		self.session = requests.session()
		self.session.verify = verify
		self.session.headers.update({'accept': 'application/json'})
		self.session.headers.update({'Authorization': f'Token {api_key}'})

	def _get(self, url: str, params: dict = None) -> dict:
		logger.debug('GET ' + self.base_url + url + ' | ' + json.dumps(params))
		resp = self.session.get(self.base_url + url, params=params)
		logger.debug('ANSWER GET ' + self.base_url + url + ' | ' + str(resp.json()))
		return resp.json()

	def _post(self, url: str, params: dict = None, data: dict = None):
		logger.debug('POST ' + self.base_url + url + ' | ' + json.dumps(params) + ' | ' + json.dumps(data))
		resp = self.session.post(self.base_url + url, json=data, params=params)
		logger.debug('ANSWER POST ' + self.base_url + url + ' | ' + str(resp.json()))
		return resp.json()

	def _put(self, url: str, params: dict = None, data: dict or list = None):
		logger.debug('PUT ' + self.base_url + url + ' | ' + json.dumps(params) + ' | ' + json.dumps(data))
		resp = self.session.put(self.base_url + url, json=data, params=params)
		logger.debug('ANSWER PUT ' + self.base_url + url + ' | ' + str(resp.json()))
		return resp.json()

	def _patch(self, url: str, params: dict = None, data: dict or list = None):
		logger.debug('PATH ' + self.base_url + url + ' | ' + json.dumps(params) + ' | ' + json.dumps(data))
		resp = self.session.patch(self.base_url + url, json=data, params=params)
		logger.debug('ANSWER PATH ' + self.base_url + url + ' | ' + str(resp.json()))
		return resp.json()
