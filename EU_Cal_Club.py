#!/usr/bin/env python
# -*- coding: utf-8 -*-
# developed & tested with Python 3.7

from datetime import datetime, timezone
from Gpib import *

# Setup measurements, modify as needed (example is for 3458A/3457A)
class Setup:
	current_date_time = datetime.now(timezone.utc).astimezone().date().isoformat()
	measurement_filename = 'LM399 branadic ' +  current_date_time + '.csv'

	dmm_reference =	{	'gpib':		{	'address': 22,
										'timeout': gpib.T100s },

						'init':		{	'pre':		[
														'RESET',
														'TARM HOLD'
													],
										'post':		[
														'TRIG AUTO',
														'END ALWAYS',
														'TARM AUTO',
														'DISP MSG,\'                 \'',
													],
										'DC 10V':	[
														'DCV 10',
														'NPLC 100',
													],
										'OHMF 10k':	[
														'OHMF 1E4',
														'OCOMP ON',
														'DELAY 1',
														'APER 1',
													]
									},
					}

	dmm_ntc =		{	'gpib':		{	'address': 2,
										'timeout': gpib.T10s },

						'init':		{	'pre':		[
														'RESET',
														'TARM HOLD'
													],
										'post':		[
														'TRIG AUTO',
														'END ALWAYS',
														'TARM AUTO',
													],
										'NTC 10k':	[
														'OHM 1E5',
														'NPLC 10',
													]
									},
					}
	def dmm(parameters, measurement_type):
		dmm = Gpib(0, parameters['gpib']['address'])
		dmm.timeout(parameters['gpib']['timeout'])
		dmm.clear()
		
		for pre in parameters['init']['pre']:
			dmm.write(pre)

		for meas in parameters['init'][measurement_type]:
			dmm.write(meas)

		for post in parameters['init']['post']:
			dmm.write(post)
		
		return dmm
		
def main():
	dmm_reference = Setup.dmm(Setup.dmm_reference, 'DC 10V') # or 'OHMF 10k'
	dmm_ntc = Setup.dmm(Setup.dmm_ntc, 'NTC 10k')
	
	while True:
		reference_value = dmm_reference.read().strip().decode('utf-8')

		reference_value_datetime = datetime.now(timezone.utc).astimezone()

		ntc_value = dmm_ntc.read().strip().decode('utf-8')

		print(f'{reference_value_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]} > ref: {reference_value}\tntc: {ntc_value}')
	
		# Save values
		values = map(str, [reference_value_datetime.isoformat(), reference_value, ntc_value])

		with open(Setup.measurement_filename, 'a') as file_handle:
			file_handle.write(';'.join(values) + '\n')

if __name__ == '__main__':
	main()
