import os
import uuid

from progressbar import ProgressBar, UnknownLength

import nmapModule
import NetBoxAPI


class Main:
	def __init__(self, network, base_url, api_key, unprivileged):
		self.nmap = nmapModule.Scanner(network, unprivileged=unprivileged)
		self.net_box = NetBoxAPI.BaseApi(base_url, api_key)
		self.site = None
		self.post_init()

	def post_init(self):
		manufacturers = self.net_box.get_manufacturers()
		if NetBoxAPI.defaultModel.manufacturer.name not in [result['name'] for result in manufacturers['results']]:
			self.net_box.add_manufacturers(NetBoxAPI.defaultModel.manufacturer)
		device_types = self.net_box.get_device_types()
		if NetBoxAPI.defaultModel.device_type.model not in [result['display'] for result in device_types['results']]:
			self.net_box.add_device_type(NetBoxAPI.defaultModel.device_type)
		device_roles = self.net_box.get_device_roles()
		if NetBoxAPI.defaultModel.device_role.name not in [result['name'] for result in device_roles['results']]:
			self.net_box.add_device_role(NetBoxAPI.defaultModel.device_role)
		site = self.net_box.get_sites()
		self.site = site['results'][0]

	def start_nmap_scan(self):
		# bar = ProgressBar(max_value=UnknownLength, prefix='Сканирование сети ').start()
		for progressive_result in self.nmap.scan():
			if progressive_result[1]['nmap']['scanstats']['uphosts'] == progressive_result[1]['nmap']['scanstats']['totalhosts']:
				ip_address = progressive_result[0]
				host_names = progressive_result[1]['scan'][ip_address]['hostnames']
				vendor = progressive_result[1]['scan'][ip_address]['vendor']
				name = [n for n in host_names if n['name'] != '']
				if len(name) == 0:
					name = uuid.uuid4().hex
				else:
					name = name[0]['name']
				vendor = [v for k, v in vendor.items() if v != '']
				if len(vendor) == 0:
					vendor = NetBoxAPI.defaultModel.manufacturer
				else:
					vendor = NetBoxAPI.Manufacturer(name=vendor[0], description='Automatically added manufacturer')
				print(self.net_box.add_manufacturers(vendor))
				device_type = NetBoxAPI.DeviceType(
					manufacturer=vendor,
					model=NetBoxAPI.defaultModel.device_type.model,
				)
				print(self.net_box.add_device_type(device_type))
				print(self.net_box.add_ip_address(NetBoxAPI.DeviceIp4(ip_address, description='automatically found IP address')))
				device = NetBoxAPI.Device(
					name=name,
					device_type=device_type,
					role=NetBoxAPI.defaultModel.device_role,
					site=NetBoxAPI.Site(
						self.site['name'],
						self.site['slug'],
					),
					primary_ip4=NetBoxAPI.DeviceIp4(ip_address, description='automatically found IP address')
				)
				print(dict(device))
				print(self.net_box.add_device(device))
			# bar.update(bar.value + 1)
		# bar.finish()

	def add_new_device(self, device: NetBoxAPI.models.Device):
		manufacturers = self.net_box.get_manufacturers()
		if NetBoxAPI.defaultModel.manufacturer.name not in [result['name'] for result in manufacturers['results']]:
			self.net_box.add_manufacturers(NetBoxAPI.defaultModel.manufacturer)


if __name__ == '__main__':
	main_object = Main(os.getenv('network'), os.getenv('host'), os.getenv('key'), False)
	main_object.start_nmap_scan()
