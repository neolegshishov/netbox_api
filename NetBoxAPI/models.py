import urllib.parse


class Manufacturer:
	def __init__(self, name, description: str, slug: str or None = None):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = urllib.parse.quote_plus(name)
		self.description = description

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug
		yield 'description', self.description

	def __repr__(self):
		return str(dict(self))

	def __json__(self):
		return dict(self)


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

	def __repr__(self):
		return str(dict(self))

	def __json__(self):
		return dict(self)


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

	def __repr__(self):
		return str(dict(self))

	def __json__(self):
		return dict(self)


class Site:
	def __init__(self, name: str, slug: str or None = None):
		self.name = name
		self.slug = slug
		if self.slug is None:
			self.slug = urllib.parse.quote_plus(name)

	def __iter__(self):
		yield 'name', self.name
		yield 'slug', self.slug

	def __repr__(self):
		return str(dict(self))

	def __json__(self):
		return dict(self)


class DeviceIp4:
	def __init__(self, address: str, description: str, status='active'):
		self.address = address
		self.description = description
		self.status = status

	def __iter__(self):
		yield 'address', self.address
		yield 'description', self.description
		yield 'status', self.status

	def __repr__(self):
		return str(dict(self))

	def __json__(self):
		return dict(self)


class Device:
	def __init__(
			self,
			name: str,
			device_type: DeviceType,
			role: DeviceRole,
			site: Site,
			primary_ip4: DeviceIp4 or None,
	):
		self.device_type = device_type
		self.role = role
		self.site = site
		self.primary_ip4 = primary_ip4
		self.name = name.replace('.', '_')

	def __iter__(self):
		yield 'name', self.name
		yield 'device_type', dict(self.device_type)
		yield 'role', dict(self.role)
		yield 'site', dict(self.site)
		yield 'primary_ip4', dict(self.primary_ip4)

	def __repr__(self):
		return str(dict(self))

	def __json__(self):
		return dict(self)

