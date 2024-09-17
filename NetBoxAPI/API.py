import requests

# TODO: создавать (если не задан другой) производителя "Unknown" для устройств, у которых не определен производитель


class BaseApi:
	def __init__(self, base_url: str, api_key: str):
		self.base_url = base_url
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

	def _post(self, url: str, params: dict = None) -> dict:
		resp = self.session.post(self.base_url + url, params=params)
		resp.raise_for_status()
		return resp.json()
