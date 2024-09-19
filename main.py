import NetBoxAPI
import os
import nmapModule
from progressbar import ProgressBar, UnknownLength


class Main:
	def __init__(self, network, base_url, api_key, unprivileged):
		self.nmap = nmapModule.Scanner(network, unprivileged=unprivileged)
		self.net_box = NetBoxAPI.BaseApi(base_url, api_key)
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

# ('16.0.0.1', {'nmap': {}, 'scan': {'16.0.0.1': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '16.0.0.1'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'syn-ack'}}}})

	def start_nmap_scan(self):
		bar = ProgressBar(max_value=UnknownLength, prefix='Сканирование сети ').start()
		for progressive_result in self.nmap.scan():
			if progressive_result[1]['nmap']['scanstats']['uphosts'] == progressive_result[1]['nmap']['scanstats']['totalhosts']:
				print(progressive_result)
				ip_address = progressive_result[0]
				host_names = progressive_result[1]['scan'][ip_address]['hostnames']
				vendor = progressive_result[1]['scan']['vendor']
				print(ip_address, host_names, vendor)
			bar.update(bar.value + 1)
		bar.finish()


if __name__ == '__main__':
	main_object = Main(os.getenv('network'), os.getenv('host'), os.getenv('key'), True)
	main_object.start_nmap_scan()
