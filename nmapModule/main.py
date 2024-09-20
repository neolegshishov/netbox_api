import nmap
import socket
from loguru import logger


class Scanner:
	def __init__(self, network: None or str = None, aggressively: bool = False, mask: int = 24, unprivileged: bool = False):
		if network is None:
			network = socket.gethostbyname(socket.gethostname())
			logger.warning('you have not installed the network, the program detected: {}'.format(network))
		self.network = network + '/' + str(mask)
		self.aggressively = aggressively
		self.unprivileged = unprivileged
		self.nmap = nmap.PortScannerYield()

	def scan(self):
		return self.nmap.scan(
			self.network,
			arguments=('-A' if self.aggressively else '-sn') + (' --unprivileged' if self.unprivileged else '')
		)
