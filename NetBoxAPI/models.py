import urllib.parse


class Manufacturer:
	def __init__(self, name, slug: str or None = None, description: str or None = None):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = urllib.parse.quote_plus(name)
		self.description = description

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug
		yield 'description', self.description


class DeviceType:
	def __init__(self, manufacturer: Manufacturer, model: str, slug: str or None = None):
		self.manufacturer = manufacturer
		self.model = model
		self.slug = slug
		if self.slug is None:
			self.slug = urllib.parse.quote_plus(model)

	def __iter__(self):
		yield 'manufacturer', dict(self.manufacturer),
		yield 'model', self.model
		yield 'slug', self.slug


class DeviceRole:
	def __init__(self, name: str, slug: str or None = None, color: str = '00ff00'):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = urllib.parse.quote_plus(name)
		self.color = color

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug
		yield 'color', self.color


class Site:
	def __init__(self, name: str, slug: str or None = None):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = urllib.parse.quote_plus(name)

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug


class DeviceIp4:
	def __init__(self, address: str, description: str or None = None):
		self.address = address
		self.description = description

	def __iter__(self):
		yield 'address', self.address
		yield 'description', self.description


class Device:
	def __init__(
			self,
			name: str,
			device_type: DeviceType,
			role: DeviceRole,
			site: Site,
			face: str,
			address: DeviceIp4 or None,
	):
		if face not in ('front', 'rear'):
			raise ValueError('Face must be either front or rear')
		self.device_type = device_type
		self.role = role
		self.site = site
		self.face = face
		self.address = address
		self.name = name

	def __iter__(self):
		yield 'name', self.name
		yield 'device_type', self.device_type
		yield 'role', self.role
		yield 'site', self.site
		yield 'face', self.face
		yield 'address', self.address

