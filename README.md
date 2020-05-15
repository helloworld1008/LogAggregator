# LogAggregator - Collect logs between two timestamps

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
