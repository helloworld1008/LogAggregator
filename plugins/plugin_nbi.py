#!/usr/bin/env python


from PluginManager import Plugin
import re

class nbi(Plugin):

	log_timestamp_pattern = re.compile('^(\d{4})\-(\d{2})\-(\d{2}) (\d{2}):(\d{2}):(\d{2}).*$')

	year_position = 1
	month_position = 2
	day_position = 3
	hour_position = 4
	minute_position = 5
	second_position = 6

	log_filename_pattern = 'nbi.log*'
