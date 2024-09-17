import nmapModule

nmap = nmapModule.Scanner('192.168.1.0')
for progressive_result in nmap.scan():
	# if progressive_result[1]['nmap']['scanstats']['uphosts'] == '1':
	print(progressive_result)
