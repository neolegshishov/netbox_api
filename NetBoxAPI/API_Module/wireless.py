from .Base import BaseObject
from NetBoxAPI.models import *


class WirelessLinksAPI(BaseObject):
	def add_wireless_link(self, link: WirelessLink):
		return self._post('/wireless/wireless-links/', data=dict(link))

	def get_wireless_links(self):
		return self._get('/wireless/wireless-links/')


class Wireless(WirelessLinksAPI):
	pass
