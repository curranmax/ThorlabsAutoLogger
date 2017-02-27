
# Requires PyVisa, PyVisa-py, and ThorlabsPM100
# PyVisa : https://pyvisa.readthedocs.io/en/stable/
# PyVisa-py : https://pyvisa-py.readthedocs.io/en/latest/
# PuUSB : http://walac.github.io/pyusb/
# ThorlabsPM100 : https://pypi.python.org/pypi/ThorlabsPM100

import visa
from ThorlabsPM100 import ThorlabsPM100

class PowerMeter:
	def __init__(self, resource_id = ''):
		if resource_id == '':
			# Current default resource_id for our power meter
			resource_id = 'USB0::4883::32888::P0015193::0::INSTR'
		self.resource_id = resource_id
		self.power_meter = None

		self.open()

	def open(self):
		# '@py' specifies to use Pyvisa-py as the backend instead of NI VISA (which I can't installed on ubuntu)
		rm = visa.ResourceManager('@py')
		try:
			inst = rm.open_resource(self.resource_id, timeout = 1)
		except ValueError:
			raise Exception('Must have root access! Try using sudo!')

		# The ThorlabsPM100 requires \n for both types of termination. PyVisa defaults one of those to '\r'
		inst.read_termination = '\n'
		inst.write_termination = '\n'

		self.power_meter = ThorlabsPM100(inst = inst)

	def getPower(self):
		if self.power_meter != None:
			return self.power_meter.read
		else:
			raise Exception('Can\'t getPower, power_meter not opened')

	def setAverageCount(self, v):
		if self.power_meter != None:
			# This value defaults to 1. Setting it to larger values will make each log take longer.
			self.power_meter.sense.average.count = v
		else:
			raise Exception('Can\'t setAverageCount, power_meter not opened')
