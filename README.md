# LogAggregator - Collect logs between two timestamps (Under construction)

Logaggregator is python-based utility that copies all log lines between two timestamps to a new file. You can process this new log file elsewhere

## Use case
Let's say you have an application that generates a series of log files such as appserver.log.1, appserver.log.2 ..... appserver.log.n.
To investigate a problem, you may have to review all log lines between two particular timestamps. This tool will copy all log lines between the two timestamps to a new logfile even if the log lines are spread across multiple log files

## It is modular
This tool is modular. You can add modules to process a new category of log files that have a different name pattern and a different timestamp pattern in the log lines

Example: Your application added a new type of log file named serverhealth.log.N where N is any number. Additionally, this log file uses timestamp format DD-MM-YYYY hh:mm:ss

 ````bash
$ ls -l
$ serverhealth.log.5
$ serverhealth.log.4
$ serverhealth.log.3
$ serverhealth.log.2
$ serverhealth.log.1
$
$ cat serverhealth.log.1 | tail -1
$ 17-02-2020 07:34:56 - CPU Idle time below 15%

````

If you want the utility to be able to process this new log file, you will need to add a python plugin module with the name plugin_serverhealth.py to the plugins/ folder which resides in the same directory as your main script. The plugin should specify the regex pattern to locate the timestamp in the log line. It should also specify the position number of year, month, day, hour, minute, second in the matching regex pattern

````bash
$ cat plugins/plugin_serverhealth.py
#!/usr/bin/env python


from PluginManager import Plugin
import re

class serverhealth(Plugin):

        log_timestamp_pattern = re.compile('^(\d{2})\-(\d{2})\-(\d{2}) (\d{2}):(\d{2}):(\d{2}).*$')

        year_position = 3
        month_position = 2
        day_position = 1
        hour_position = 4
        minute_position = 5
        second_position = 6

        log_filename_pattern = 'serverhealth.log*'
[root@localhost plugins]# 
````

## Installation

Download the zip file of this repository to your Linux system and unzip it. 

````bash
$ ls -ltra
total 12
-rw-r--r--.  1 root root 4649 May 23 23:34 LogAggregator-master.zip
dr-xr-x---. 14 root root 4096 May 23 23:34 ..
drwxr-xr-x.  2 root root   38 May 23 23:34 .
$ unzip LogAggregator-master.zip 
Archive:  LogAggregator-master.zip
5dc3b746c632af937a322d1bc1477aec6260d709
   creating: LogAggregator-master/
  inflating: LogAggregator-master/PluginManager.py  
  inflating: LogAggregator-master/README.md  
  inflating: LogAggregator-master/logaggregator.py  
   creating: LogAggregator-master/plugins/
  inflating: LogAggregator-master/plugins/plugin_nbi.py  
  inflating: LogAggregator-master/plugins/plugin_nmstta.py  
$ ls -ltra
total 12
drwxr-xr-x.  3 root root   86 May 16 01:28 LogAggregator-master
-rw-r--r--.  1 root root 4649 May 23 23:34 LogAggregator-master.zip
dr-xr-x---. 14 root root 4096 May 23 23:34 ..
drwxr-xr-x.  3 root root   66 May 23 23:34 .
$ cd LogAggregator-master
$ ls -ltra
total 16
-rw-r--r--. 1 root root 2095 May 16 01:28 README.md
drwxr-xr-x. 2 root root   51 May 16 01:28 plugins
-rwxr-xr-x. 1 root root  761 May 16 01:28 PluginManager.py
-rwxr-xr-x. 1 root root 5670 May 16 01:28 logaggregator.py
drwxr-xr-x. 3 root root   86 May 16 01:28 .
drwxr-xr-x. 3 root root   66 May 23 23:34 ..
$

````

## Usage

````bash
$ ./logaggregator.py --help
usage: logaggregator.py [-h]
                        start_date start_time end_date end_time logs_folder
                        process_name

Extract logs between two timestamps and print them to a file.

positional arguments:
  start_date    Enter start date in yyyy-mm-dd format Eg. 2020-02-20
  start_time    Enter start time in hh:mm:ss format eg. 18:57:20
  end_date      Enter end date in yyyy-mm-dd format Eg. 2020-02-26
  end_time      Enter end time in hh:mm:ss format eg. 09:18:36
  logs_folder   Enter absolute path of logs directory eg. /var/logs
  process_name  Enter process name eg. nbi

optional arguments:
  -h, --help    show this help message and exit
  
$
````

Example:
Let's suppose you have log files of the pattern nbi.log.X stored in /app/logs folder. 
You need to collect all log lines between 30th Jan 2020 16:00:00 hrs and 18th Feb 18:50:00 hrs.

````bash

$ cd /app/logs
$ ls -ltra
total 76356
-rwxr-xr-x.  1 root root  5242903 Jan 11 19:43 nbi.log.10
-rw-r--r--.  1 root root  5242947 Jan 15 13:00 nbi.log.9
-rw-r--r--.  1 root root  5243471 Jan 22 17:19 nbi.log.8
-rw-r--r--.  1 root root  5243214 Jan 30 16:06 nbi.log.7
-rw-r--r--.  1 root root  5242908 Feb  3 19:35 nbi.log.6
-rw-r--r--.  1 root root  5242887 Feb 10 11:28 nbi.log.5
-rw-r--r--.  1 root root  5243377 Feb 18 12:40 nbi.log.4
-rw-r--r--.  1 root root  5261500 Feb 24 19:12 nbi.log.3
-rw-r--r--.  1 root root  5242923 Mar  4 12:11 nbi.log.2
-rw-r--r--.  1 root root  5243294 Mar 10 14:33 nbi.log.1
-rw-r--r--.  1 root root  1576424 Mar 12 09:06 nbi.log
drwxr-xr-x.  2 root root      259 Apr 29 09:17 .
dr-xr-x---. 14 root root     4096 May 23 23:34 ..
$
$
$ cd /home/user/LogAggregator-master
$ ls -l
total 16
-rwxr-xr-x. 1 root root 5670 May 16 01:28 logaggregator.py
-rwxr-xr-x. 1 root root  761 May 16 01:28 PluginManager.py
drwxr-xr-x. 2 root root   98 May 24 00:03 plugins
-rw-r--r--. 1 root root 2095 May 16 01:28 README.md
$
$
$ ./logaggregator.py 2020-01-30 16:00:00 2020-02-18 18:50:00 /root/mydata/ nbi
Output saved to /tmp/nbi_log_24_05_20_00_03
$
````
