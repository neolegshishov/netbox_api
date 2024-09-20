import os
import uuid

import nmapModule
import NetBoxAPI


def generate_uuid(data: str):
	return str(uuid.uuid5(uuid.NAMESPACE_DNS, data))


class Main:
	def __init__(self, network, base_url, api_key, unprivileged=True, aggressively=False):
		self.nmap = nmapModule.Scanner(network, unprivileged=unprivileged, aggressively=aggressively)
		self.net_box = NetBoxAPI.BaseApi(base_url, api_key)
		self.site = None
		self.existing_manufacturers = None
		self.existing_device_types = None
		self.existing_device_roles = None
		self.existing_devices = None
		self.existing_interfaces = None
		self.existing_ip_addresses = None
		self.existing_sites = None
		self.interface_a = None
		self.post_init()

	def post_init(self):
		self.existing_manufacturers = self.net_box.get_manufacturers()
		self.existing_device_types = self.net_box.get_device_types()
		self.existing_device_roles = self.net_box.get_device_roles()
		self.existing_devices = self.net_box.get_devices()
		self.existing_interfaces = self.net_box.get_interfaces()
		self.existing_ip_addresses = self.net_box.get_ip_addresses()
		self.existing_sites = self.net_box.get_sites()
		if NetBoxAPI.defaultModel.manufacturer.name not in [result['name'] for result in self.existing_manufacturers['results']]:
			self.net_box.add_manufacturers(NetBoxAPI.defaultModel.manufacturer)
			self.existing_manufacturers = self.net_box.get_manufacturers()
		if NetBoxAPI.defaultModel.device_type.model not in [result['display'] for result in self.existing_device_types['results']]:
			self.net_box.add_device_type(NetBoxAPI.defaultModel.device_type)
			self.existing_device_types = self.net_box.get_device_types()
		if NetBoxAPI.defaultModel.device_role.name not in [result['name'] for result in self.existing_device_roles['results']]:
			self.net_box.add_device_role(NetBoxAPI.defaultModel.device_role)
			self.existing_device_roles = self.net_box.get_device_roles()
		self.site = self.existing_sites['results'][0]

	def start_nmap_scan(self):
		for progressive_result in self.nmap.scan():
			if progressive_result[1]['nmap']['scanstats']['uphosts'] == progressive_result[1]['nmap']['scanstats']['totalhosts']:
				ip_address = progressive_result[0]
				host_names = progressive_result[1]['scan'][ip_address]['hostnames']
				name = [n for n in host_names if n['name'] != '']
				vendor = progressive_result[1]['scan'][ip_address]['vendor']
				vendor = [v for k, v in vendor.items() if v != '']
				self.add_new_device(ip_address, name, vendor)

	def add_new_device(self, ip_address: str, name: list, vendor: list):
		if len(vendor) == 0:
			vendor = NetBoxAPI.defaultModel.manufacturer
		else:
			vendor = NetBoxAPI.Manufacturer(name=vendor[0], description='Automatically added manufacturer')
		if vendor.name not in [result['name'] for result in self.existing_manufacturers['results']]:
			self.net_box.add_manufacturers(vendor)
			self.existing_manufacturers = self.net_box.get_manufacturers()
		device_type = NetBoxAPI.DeviceType(
			manufacturer=vendor,
			model=NetBoxAPI.defaultModel.device_type.model,
		)
		if [device_type.model, device_type.manufacturer.name] not in [[result['display'], result['manufacturer']['display']] for result in self.existing_device_types['results']]:
			self.net_box.add_device_type(device_type)
			self.existing_device_types = self.net_box.get_device_types()
		device = NetBoxAPI.Device(
			name='',
			device_type=device_type,
			role=NetBoxAPI.defaultModel.device_role,
			site=NetBoxAPI.Site(
				self.site['name'],
				self.site['slug']
			)
		)
		if len(name) == 0:
			name = generate_uuid(str(dict(device)))
		else:
			name = name[0]['name']
		device.name = name
		if device.name not in [result['name'] for result in self.existing_devices['results']]:
			device_id = self.net_box.add_device(device)['id']
			self.existing_devices = self.net_box.get_devices()
		else:
			device_id = [result['id'] for result in self.existing_devices['results'] if result['name'] == device.name][0]
		interface = NetBoxAPI.Interface(device.name + '_interface', device)
		if interface.name not in [result['name'] for result in self.existing_interfaces['results']]:
			interface_id = self.net_box.add_interface(interface)['id']
			self.existing_interfaces = self.net_box.get_interfaces()
		else:
			interface_id = [result['id'] for result in self.existing_interfaces['results'] if result['name'] == interface.name][0]
		ip_address_object = NetBoxAPI.DeviceIp4(ip_address, description='automatically found IP address')
		ip_address_object.assigned_object_id = interface_id
		if ip_address_object.address + '/32' not in [result['address'] for result in self.existing_ip_addresses['results']]:
			address_id = self.net_box.add_ip_address(ip_address_object)['id']
			self.existing_ip_addresses = self.net_box.get_ip_addresses()
		else:
			address_id = [result['id'] for result in self.existing_ip_addresses['results'] if result['address'] == ip_address_object.address + '/32'][0]
		self.net_box.assign_primary_ip(device_id, address_id)
		if ip_address != '192.168.1.1':
			self.add_connection(interface)
		else:
			self.interface_a = interface

	def add_connection(self, interface_b):
		if self.interface_a is None:
			return
		wireless_link = NetBoxAPI.WirelessLink(self.interface_a, interface_b)
		self.net_box.add_wireless_link(wireless_link)


if __name__ == '__main__':
	main_object = Main(os.getenv('network'), os.getenv('host'), os.getenv('key'), False, aggressively=True)
	main_object.start_nmap_scan()
