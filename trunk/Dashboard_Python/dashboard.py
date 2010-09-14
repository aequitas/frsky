import os,sys,serial,threading,time, ConfigParser
from collections import deque

from optparse import OptionParser
from FrSky import *

		
		
op = OptionParser()
op.add_option("-i",dest="infile",
	help="open FILE for parsing", default=None)
op.add_option("-c",dest="csvLogging",
	help="Log to a CSV data file", default=None)
op.add_option("-a",dest="ascLogging",
	help="Log to a human readable framefile",metavar="FILE")
op.add_option("-r",dest="rawLogging",
	help="Log to a raw file")

op.add_option("-m",dest="movingaverage",
	help="set the numbers of samples to use for moving average calculations, use 1 for no filtering",metavar="#",default=1)
op.add_option("-p","--port",dest="port",
	help="Use serialport PORT",metavar="PORT",default=None)	
(options,args) = op.parse_args()

# myServer = FrSkyServer(options)
# myServer.start()
# myServer.join()

config = ConfigParser.ConfigParser()
config.readfp(open('dashboard.cfg'))

myServer = FrSkyServerX(options,config)
myServer.master.title('FrSky Dashboard')
myServer.mainloop()
myServer.start()
myServer.join()


#myParser = FrSkyParser()
