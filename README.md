# LogAggregator - Collect logs between two timestamps

Logaggregator is python-based utility that copies all log lines between two timestamps to a new file. You can process this new log file elsewhere

## Use case
Let's say you have an application that generates a series of log files such as appserver.log.1, appserver.log.2 ..... appserver.log.n.
To investigate a problem, you may have to review all log lines between two particular timestamps. This tool will copy all the log lines between the two timestamps to a new logfile even if the log lines are spread across multiple log files


