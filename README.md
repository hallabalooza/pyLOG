# pyLOG

## Abstract

pyLOG is a Python 3.5 implementation of a custom Python logging RotatingFileHandler that rolls over if a certain
time intervall changes. E.g. if the intervall is set to 'hour' and the logging starts at 05.11.2017
(calender week 44) 11:46:23 and stops at 05.11.2017 13:13:45, there will be logging files
* 20171105_44_110000 containing all logging events from 11:46:23 to 11:59:59,
* 20171105_44_120000 containing all logging events from 12:00:00 to 12:59:59 and
* 20171105_44_130000 containing all logging events from 13:00:00 to 13:13:45.
Of course the format string is configurable.
