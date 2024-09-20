from NetBoxAPI.models import *
from .Base import BaseObject


class IPAddress(BaseObject):
	def get_ip_addresses(self):
		return self._get('/ipam/ip-addresses/')

	def add_ip_address(self, ip_address: DeviceIp4):
		return self._post('/ipam/ip-addresses/', data=dict(ip_address))


class IPAM(IPAddress):
	pass
