
from power_meter import PowerMeter
import time
from math import log
import argparse

def convertWattsToDbm(v):
	return 30.0 + 10 * log(v, 10)

# test_length - float greater than 0 - length of test in SECONDS
# TODO allow for a ctrl+c interrupt or something
def autoLog(test_length, out_file):
	num_iters = 0

	power_meter = PowerMeter()
	power_meter.setAverageCount(1)

	if out_file != '':
		f = open(out_file, 'w')
		f.write('time(s) power(dBm)\n')
	else:
		f = None

	start_time = time.time()
	while True:
		power = power_meter.getPower()
		num_iters += 1

		end_time = time.time()
		delta_time = end_time - start_time
		
		if f != None:
			f.write(str(delta_time) + ' ' + str(convertWattsToDbm(power)) + '\n')
		else:
			print convertWattsToDbm(power), 'dBm'
		
		if delta_time > test_length:
			break
	
	if f != None:
		f.close()

	print 'Average time per log:', (end_time - start_time) * 1000.0 / float(num_iters), 'ms'
	print 'Number of logs:', num_iters

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Constantly reads from power meter, and writes data to a file')

	parser.add_argument('-tl', '--test_length', metavar = 'TEST_LENGTH', type = float, nargs = 1, default = [1.0], help = 'Length of the test in seconds')
	parser.add_argument('-f', '--out_file', metavar = 'OUT_FILE_NAME', type = str, nargs = 1, default = [''], help = 'File to write output to. If no file given, then power is printed to stdout')
	
	args = parser.parse_args()

	test_length = args.test_length[0]
	out_file = args.out_file[0]

	autoLog(test_length, out_file)

