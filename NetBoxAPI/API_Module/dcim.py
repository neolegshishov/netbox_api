from NetBoxAPI.models import *
from .Base import BaseObject


class DeviceAPI(BaseObject):
	def get_devices(self):
		return self._get('/dcim/devices/')

	def add_device(self, device: Device):
		return self._post('/dcim/devices/', data=dict(device))

	def update_device(self, device: Device):
		return self._put('/dcim/devices/', data=[dict(device)])

	def assign_primary_ip(self, device_id: int, ip_address_id: int):
		data = {
			'primary_ip4': ip_address_id,
		}
		self._patch(f'/dcim/devices/{device_id}/', data=data)


class DeviceTypeAPI(BaseObject):
	def get_device_types(self):
		return self._get('/dcim/device-types/')

	def add_device_type(self, device_type: DeviceType):
		return self._post('/dcim/device-types/', data=dict(device_type))


class ManufacturersAPI(BaseObject):
	def add_manufacturers(self, manufacturer: Manufacturer):
		return self._post('/dcim/manufacturers/', data=dict(manufacturer))

	def get_manufacturers(self):
		return self._get('/dcim/manufacturers/')


class DeviceRolesAPI(BaseObject):
	def get_device_roles(self):
		return self._get('/dcim/device-roles/')

	def add_device_role(self, role: DeviceRole):
		return self._post('/dcim/device-roles/', data=dict(role))


class SitesAPI(BaseObject):
	def get_sites(self):
		return self._get('/dcim/sites/')


class InterfaceAPI(BaseObject):
	def add_interface(self, interface: Interface):
		return self._post('/dcim/interfaces/', data=dict(interface))

	def get_interfaces(self):
		return self._get('/dcim/interfaces/')


class CablesAPI(BaseObject):
	def add_cable(self, cable: Cable):
		return self._post('/dcim/cables/', data=dict(cable))

	def get_cables(self):
		return self._get('/dcim/cables/')


class DCIM(DeviceAPI, DeviceTypeAPI, ManufacturersAPI, DeviceRolesAPI, SitesAPI, InterfaceAPI, CablesAPI):
	pass
