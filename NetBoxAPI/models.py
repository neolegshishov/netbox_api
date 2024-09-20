import string

SAFE_LETTERS = string.ascii_letters + string.digits


def make_slug(data: str):
	return ''.join(['_' if d not in SAFE_LETTERS else d for d in data.lower()])

class BaseModel:
	def __repr__(self):
		return str(dict(self))

	def __json__(self):
		return dict(self)


class Manufacturer(BaseModel):
	def __init__(self, name, description: str, slug: str or None = None):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = make_slug(name)
		self.description = description

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug
		yield 'description', self.description


class DeviceType(BaseModel):
	def __init__(self, manufacturer: Manufacturer, model: str, slug: str or None = None):
		self.manufacturer = manufacturer
		self.model = model
		self.slug = slug
		if self.slug is None:
			self.slug = make_slug(model)

	def __iter__(self):
		yield 'manufacturer', dict(self.manufacturer),
		yield 'model', self.model
		yield 'slug', self.slug


class DeviceRole(BaseModel):
	def __init__(self, name: str, slug: str or None = None, color: str = '00ff00'):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = make_slug(name)
		self.color = color

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug
		yield 'color', self.color


class Site(BaseModel):
	def __init__(self, name: str, slug: str or None = None):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = make_slug(name)

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug


class DeviceIp4(BaseModel):
	def __init__(self, address: str, description: str, status='active'):
		self.address = address
		self.description = description
		self.status = status
		self.object_id = None
		self.assigned_object_type = 'dcim.interface'
		self.assigned_object_id = None

	def __iter__(self):
		yield 'address', self.address
		yield 'description', self.description
		yield 'status', self.status
		if self.object_id is not None:
			yield 'id', self.object_id
		if self.assigned_object_id is not None:
			yield 'assigned_object_type', self.assigned_object_type
			yield 'assigned_object_id', self.assigned_object_id


class Device(BaseModel):
	def __init__(
			self,
			name: str,
			device_type: DeviceType,
			role: DeviceRole,
			site: Site,
	):
		self.device_type = device_type
		self.role = role
		self.site = site
		self.name = name.replace('.', '_')
		self.primary_ip4 = None
		self.object_id = None

	def __iter__(self):
		yield 'name', self.name
		yield 'device_type', dict(self.device_type)
		yield 'role', dict(self.role)
		yield 'site', dict(self.site)
		if self.primary_ip4 is not None:
			yield 'primary_ip4', dict(self.primary_ip4)
		if self.object_id is not None:
			yield 'id', self.object_id


class Interface(BaseModel):
	def __init__(
			self,
			name: str,
			device: Device,
			interface_type: str = 'other-wireless',
	):
		self.device = device
		self.interface_type = interface_type
		self.name = name.replace('.', '_')

	def __iter__(self):
		yield 'name', self.name
		yield 'device', dict(self.device)
		yield 'type', self.interface_type


class Cable(BaseModel):
	def __init__(
			self,
			interface_a_id: int,
			interface_b_id: int
	):
		self.interface_a_id = interface_a_id
		self.interface_b_id = interface_b_id

	def __iter__(self):
		yield 'interface_a', self.interface_a_id
		yield 'interface_b', self.interface_b_id


class WirelessLink(BaseModel):
	def __init__(
			self,
			interface_a: Device,
			interface_b: Device
	):
		self.interface_a = interface_a
		self.interface_b = interface_b

	def __iter__(self):
		yield 'interface_a', dict(self.interface_a)
		yield 'interface_b', dict(self.interface_b)
