import NetBoxAPI

# nmap = nmapModule.Scanner('192.168.1.0')
# for progressive_result in nmap.scan():
# 	print(progressive_result)
# 	if progressive_result[1]['nmap']['scanstats']['uphosts'] == '1':
# 		print(progressive_result[1]['nmap']['scanstats']['uptime'])

# devices = session.get_devices()
manufacturers = session.get_manufacturers()

if NetBoxAPI.defaultModel.manufacturer.name not in [result['name'] for result in manufacturers['results']]:
	print(session.add_manufacturers(NetBoxAPI.defaultModel.manufacturer))

device_types = session.get_device_types()
if NetBoxAPI.defaultModel.device_type.model not in [result['display'] for result in device_types['results']]:
	print(session.add_device_type(NetBoxAPI.defaultModel.device_type))
