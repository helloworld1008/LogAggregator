#!/usr/bin/env python

import sys, re, datetime, os, fnmatch, argparse

from PluginManager import PluginManager

class LogAggregator:


	def __init__(self, start_date, start_time, end_date, end_time, logs_folder, process_name):


		if self.validate_date(start_date) and self.validate_time(start_time) and\
		   self.validate_date(end_date) and self.validate_time(end_time): 

			start_timestamp = datetime.datetime.combine(self.validate_date(start_date),self.validate_time(start_time))

			end_timestamp = datetime.datetime.combine(self.validate_date(end_date),self.validate_time(end_time))

			
			if end_timestamp > start_timestamp:

				self.start_timestamp = start_timestamp
				self.end_timestamp = end_timestamp

			else:

				print "End timestamp must be greater than Start timestamp"
				sys.exit(0)


		if self.validate_logs_folder(logs_folder):

			self.logs_folder = logs_folder


		self.log_plugin =  self.verifyPluginAvailability(process_name)


		#self.file_dict = self.get_file_list()



	def validate_date(self, input_date):

		search_pattern = re.search(r'^(\d{4})-(\d{2})-(\d{2})$', input_date)

		if search_pattern is None:

			print "\n" + input_date + ": " + "Invalid date pattern!!! You must enter date in yyyy-mm-dd format\n"
			sys.exit(0)

		else:

			yr = int(search_pattern.group(1))
			mt = int(search_pattern.group(2))
			dy = int(search_pattern.group(3))

			try:

				dt = datetime.datetime(yr, mt, dy)

			except ValueError as e:

				print "\n" + input_date + ": " + str(e) + "\n"
				sys.exit(0)
	
		return dt


	def validate_time(self, input_time):

		search_pattern = re.search(r'^(\d{2}):(\d{2}):(\d{2})$', input_time)

		if search_pattern is None:

			print "\n" + input_time + ": " + "Invalid time pattern!!! You must enter time in hh:mm:ss format\n"
			sys.exit(0)

		else:

			hr = int(search_pattern.group(1))
			mn = int(search_pattern.group(2))
			sc = int(search_pattern.group(3))

			try:

				tm = datetime.time(hr, mn, sc)

			except ValueError as e:

				print "\n" + input_time + ": " + str(e) + "\n"
				sys.exit(0)

		return tm


	def validate_logs_folder(self, folder):

		try:

			if os.stat(folder):
				
				if not os.access(folder, os.R_OK) or not os.access(folder, os.X_OK):

					print "\nThe path of the logs folder you've entered does not have read or execute permissions\n"


					sys.exit(0)

		except OSError as e:

			print "\n{0}\n".format(e)

			sys.exit(0)


		return True


	def verifyPluginAvailability(self, process_name):

		plugin_manager = PluginManager()

		plugin_found_flag = 0

		for plugin in plugin_manager.plugins:

			if plugin.__class__.__name__ == process_name:

				plugin_found_flag = 1
				break

		if plugin_found_flag == 0:

			print "No plugin found for {0} process logs".format(process_name)

			sys.exit(0)

		return plugin


	def logLinesExtractor(self):


		output_filename = '/tmp/' + self.log_plugin.__class__.__name__ + '_log_' + datetime.datetime.now().strftime("%d_%m_%y_%H_%M")

		fwo = open(output_filename, 'w')
 
		for file in self.get_file_list():

			for line in open(file):

				#print line
	
				pattern_matching_result = self.log_plugin.log_timestamp_pattern.match(line)

				if pattern_matching_result:

					yr = pattern_matching_result.group(self.log_plugin.year_position)
					if len(yr) == 2:
						yr = int('20' + yr)
					else:
						yr = int(yr)

					mt = int(pattern_matching_result.group(self.log_plugin.month_position))
					dt = int(pattern_matching_result.group(self.log_plugin.day_position))

					hr = int(pattern_matching_result.group(self.log_plugin.hour_position))
					mn = int(pattern_matching_result.group(self.log_plugin.minute_position))
					sc = int(pattern_matching_result.group(self.log_plugin.second_position))

					line_timestamp = datetime.datetime(yr,mt,dt,hr,mn,sc)

					if line_timestamp >= self.start_timestamp and line_timestamp <= self.end_timestamp:

						#print line
						fwo.write(line)

		fwo.close()
		print "Output saved to {0}".format(output_filename)
			
	
	def get_file_list(self):

		file_dict = {}
		file_list = []

		os.chdir(self.logs_folder)

		for file in os.listdir(self.logs_folder):

			if fnmatch.fnmatch(file, self.log_plugin.log_filename_pattern):

				file_dict[os.stat(file).st_mtime] = file

		#file_modification_timestamps = file_dict.keys()

		#file_modification_timestamps.sort()


		if not file_dict:

			print "\nNo nbi.log files found in logs folder\n"

			sys.exit(0)

		for key in sorted(file_dict.keys()):

			file_list.append(file_dict[key])			

		return file_list


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Extract logs between two timestamps and print them to a file.") 

	parser.add_argument("start_date", help="Enter start date in yyyy-mm-dd format Eg. 2020-02-20")

	parser.add_argument("start_time", help="Enter start time in hh:mm:ss format eg. 18:57:20")

	parser.add_argument("end_date", help="Enter end date in yyyy-mm-dd format Eg. 2020-02-26")

	parser.add_argument("end_time", help="Enter end time in hh:mm:ss format eg. 09:18:36")

	parser.add_argument("logs_folder", help="Enter absolute path of logs directory eg. /var/logs")

	parser.add_argument("process_name", help="Enter process name eg. nbi")

	args = parser.parse_args()

	l = LogAggregator(args.start_date, args.start_time, args.end_date, args.end_time, args.logs_folder, args.process_name)

	l.logLinesExtractor()
