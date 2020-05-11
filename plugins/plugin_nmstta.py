#!/usr/bin/env python


from PluginManager import Plugin
import re

class nmstta(Plugin):

        log_timestamp_pattern = re.compile('^.*?(\d{2})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2}).*$')

        year_position = 3
        month_position = 2
        day_position = 1
        hour_position = 4
        minute_position = 5
        second_position = 6

        log_filename_pattern = 'NMSTTA.log*'
