from .models import Manufacturer, DeviceType, DeviceRole

manufacturer = Manufacturer(name='Unknown', description='manufacturer was not identified during scanning')
device_type = DeviceType(manufacturer=manufacturer, model='Unknown')
device_role = DeviceRole(name='Unknown')
