import os,sys,serial,threading,time,msvcrt,math
from collections import deque
from Tkinter import *

import tkFont


from optparse import OptionParser



class Debug:
	def __init__(self,str=""):
		print str


class Widget(Frame):
	def __init__(self,master=None,**args):
		Frame.__init__(self,master,borderwidth=2,relief=GROOVE, width=300,height=250)
		self.width=self['width']
		self.height=self['height']
		self.borderwidth=self['borderwidth']
		
		self.hForcer = Frame(self,width=self.width,height=1)
		self.hForcer.grid(row=0,column=0,columnspan=10)
		
		self.vForcer = Frame(self,height=self.height,width=1)
		self.vForcer.grid(row=0,column=0,rowspan=10)
		
		self.helv68 = tkFont.Font ( family="Helvetica",size=68, weight="bold" )

	def resize(self,newWidth=None,newHeight=None):
		if newWidth!=None:
			self.hForcer.configure(width=newWidth)
			#self.width = self['width']
			self.width = newWidth
		if newHeight!=None:
			self.vForcer.configure(height=newHeight)
			#self.height = self['height']
			
			self.height=newHeight
	
		try:
			self.subResize(newWidth,newHeight)
		except:
			pass
		
		
class TimeFrame(Widget):
	def __init__(self,master=None):
		Widget.__init__(self,master)		
	
		self.startTime = time.time()
		self.runningTime = 0		
		
		self.createWidgets()
		
	def subResize(self,newWidth,newHeight):
		
		fontFactor = float(self.width)/300
		fontSize = int(fontFactor*68)
		self.lblMain.configure(font=tkFont.Font ( family="Helvetica",size=fontSize, weight="bold" ))
		
	def createWidgets(self):
		self.lblTop = Label(self,text="Timer")
		self.lblTop.grid(row=0,column=1)
		
		self.lblMain = Label(self,text="00:00",font=self.helv68)
		self.lblMain.grid(row=1,column=0,columnspan=10)
		self.lblMain.after(1000,self.tick)
		
		self.btnResetTimer = Button(self,text='Reset',command=self.resetTimer)
		self.btnResetTimer.grid(row=2,column=0,columnspan=10,sticky=E+W)
	
	def tick(self):
		minutes = int(self.runningTime/60)
		secs = "%s" % int(self.runningTime-(minutes*60))
		
		minSec = "{:0>2}:{:0>2}".format(minutes,secs)
		
		self.lblMain.config(text="%s" % minSec)
		self.lblMain.after(1000,self.tick)

	def resetTimer(self):
		print "Reset timer"
		self.startTime=time.time()
		self.runningTime = 0
		minutes = int(self.runningTime/60)
		secs = "%s" % int(self.runningTime-(minutes*60))
		
		minSec = "{:0>2}:{:0>2}".format(minutes,secs)
		self.lblMain.config(text="%s" % minSec)
		
	def update(self):
		self.currentTime = time.time()
		self.runningTime = self.currentTime-self.startTime

		
class InfoFrame(Widget):
	def __init__(self,master=None,options=None):
		Widget.__init__(self,master)
		self.options=options
		
		
		self.varRawLoggingEnabled = IntVar()
		self.varRawLoggingEnabled.set(1)
		self.varCsvLoggingEnabled = IntVar()
		self.varCsvLoggingEnabled.set(1)
		self.varAscLoggingEnabled = IntVar()
		self.varAscLoggingEnabled.set(0)


		
		self.createWidgets()
	
	def createWidgets(self):
		self.sectionwidth = (self.width-(6*self.borderwidth))/3
		
		self.lblTop = Label(self,text="Information")
		self.lblTop.grid(row=0,column=1)

		self.frameLogging = LabelFrame(self,text="Logging",width=self.sectionwidth)
		self.frameLogging.grid(row=1,column=8)
		
		
		self.lblLoggingFolderD = Label(self.frameLogging,text="Folder:")
		self.lblLoggingFolderD.grid(row=0,column=0,sticky=W)
		
		self.lblLoggingFolder = Label(self.frameLogging,text="./logs/")
		self.lblLoggingFolder.grid(row=1,column=0,sticky=W)
		
		
		self.lblLoggingPrefixD = Label(self.frameLogging,text="Prefix:")
		self.lblLoggingPrefixD.grid(row=2,column=0,sticky=W)
		
		self.lblLoggingPrefix = Label(self.frameLogging,text="")
		self.lblLoggingPrefix.grid(row=3,column=0,sticky=W)
		
		self.chkRawLogging = Checkbutton(self.frameLogging, variable=self.varRawLoggingEnabled,command=self.__toggleRawLogging,text="Raw [.RAW]")
		self.chkRawLogging.grid(row=4,column=0,sticky=W)
		
		self.chkCsvLogging = Checkbutton(self.frameLogging, variable=self.varCsvLoggingEnabled,command=self.__toggleCsvLogging,text="CSV [.CSV]")
		self.chkCsvLogging.grid(row=5,column=0,sticky=W)
		
		self.chkAscLogging = Checkbutton(self.frameLogging, variable=self.varAscLoggingEnabled,command=self.__toggleAscLogging,text="ASCII [.ASC]")
		self.chkAscLogging.grid(row=6,column=0,sticky=W)
		
		self.rowconfigure(9,weight=1)
		self.columnconfigure(7,weight=1)
		
	def __toggleRawLogging(self):
		print "Toggle Raw Logging"
		self.setLoggingPrefix(self.loggingPrefix)
		
	def __toggleCsvLogging(self):
		print "Toggle CSV Logging"
		self.setLoggingPrefix(self.loggingPrefix)
		
	def __toggleAscLogging(self):
		print "Toggle ASC Logging"
		self.setLoggingPrefix(self.loggingPrefix)
	
	def setLoggingPrefix(self,prefix):
		self.loggingPrefix=prefix
		
		self.lblLoggingPrefix.config(text=prefix)
		
		if self.varRawLoggingEnabled.get()==1:
			self.options.rawLogging=True
		else:
			self.options.rawLogging=False
		
		if self.varCsvLoggingEnabled.get()==1:
			self.options.csvLogging=True
		else:
			self.options.csvLogging=False
		
		if self.varAscLoggingEnabled.get()==1:
			self.options.ascLogging=True
		else:
			self.options.ascLogging=False
		
		
class AdFrame(Widget):
	
	def __init__(self,master=None):
		Widget.__init__(self,master)
		
		self.master = master
		#self.grid()
		self.unit=""
				
		# Control Variables
		self.varEnabled = IntVar()
		self.varEnabled.set(0)
		self.enabled=False
		self.varValue = DoubleVar()
		
		# Generate the GUI
		self.createWidgets()
	
	def subResize(self,newWidth,newHeight):
		
		fontFactor = float(self.width)/300
		fontSize = int(fontFactor*68)
		self.lblMain.configure(font=tkFont.Font ( family="Helvetica",size=fontSize, weight="bold" ))

	def createWidgets(self):
		
		#self.myconfig = self.config()
		#self.width =  self.myconfig["width"][-1]
		#self.width=self['width']
		#self.height=self['height']
		print "height: %s" % self.height
		#self.borderwidth= self.myconfig["borderwidth"][-1]
		#self.borderwidth=self['borderwidth']
		
		#self.hForcer = Frame(self,width=self.width,height=1)
		#self.hForcer.grid(row=0,column=0,columnspan=10)
		
		#self.vForcer = Frame(self,height=self.height,width=1)
		#self.vForcer.grid(row=0,column=0,rowspan=10)
		
		
		self.lblTop = Label(self,text="")
		self.lblTop.grid(row=0,column=1)
		
		self.chkSelfEnabled = Checkbutton(self, variable=self.varEnabled,command=self.__toggleEnabled)
		self.chkSelfEnabled.grid(row=0,column=0)
		
		self.lblMain = Label(self,text="2.40V",textvariable=self.varValue,font=self.helv68)
		self.lblMain.grid(row=1,column=0,columnspan=10)
		
		self.progBar = Frame(self,background='blue', width=0,height=10,borderwidth=0)
		self.progBar.grid(row=2,column=0,columnspan=10,sticky=W)
		
	def setName(self,str):
		self.lblTop.config(text=str)
	def setUnit(self,unit=""):
		self.unit=unit
		
	def __toggleEnabled(self):
		#print "Click: %s" % self.varEnabled.get()
		if self.varEnabled.get()==1:
			self.enable()
		else:
			self.disable()
		pass
		
		
		
	def disable(self):
		self.enabled=False
		self.varEnabled.set(0)
		self.lblMain.config(foreground="#cccccc")
		self.setProgress(0)
		pass
		
	def enable(self):
		self.enabled=True
		self.varEnabled.set(1)
		self.lblMain.config(foreground="black")
		pass
		
	def setEnabled(self,en):
		if en:
			self.enable()
		else:
			self.disable()
	
	def setMinMax(self,min,max): # Sets minimum and maximum values that this widget will show
		
		self.valueMin=min
		self.valueMax=max
		self.valueRange= max-min
		pass
	
	def setValue(self,value): # Sets the value the widget will show
		if self.varEnabled.get()==1:
			self.value=value
			prc = self.value*100/self.valueRange
			# need to update lblMain
			self.varValue.set("{:.2f}%s".format(value) % self.unit)
			self.setProgress(prc)
			pass
		
	def setProgress(self,prc=0):
		
		newWidth = (self.width-(4*self.borderwidth))*prc/100
		self.progBar.config(width=newWidth)
		if prc<50:
			self.progBar.config(background='red')
		else:
			self.progBar.config(background='blue')
		
		
class FrSkyParser:
	# Moved to redmine
	# Publics:
	TotalSampleCount = 0
	CurrentSampleCount = 0
	
	FrameArray = {}
	UserFrameArray = {}
	UnparsedFrameArray = {}
	JitterFrameArray = {}
	ADArray = {}
	CurrentADData = {}
	MaxDeviationAllowed = 0
	
	
	
	# Private
	#inFile = None
	inFileContents = ""
	inFileContentLength = 0
	progress = 0
	tmpAD1dev = 0
	tmpAD2dev = 0
	
	tmpAD1 = deque([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],10)
	tmpAD2 = deque([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],10)
	#tmpAD1 = deque(None,10)
	
	def __init__(self,options):
		#Debug("#Constructor")
		self.options = options
		self.FrameArray = {}
		self.UserFrameArray = {}
		self.UnparsedFrameArray = {}
		#self.JitterFrameArray = {}
		self.ADArray = {}
		self.CurrentADData = {}
		self.setMovingAverageSize(int(options.movingaverage))
		pass
	
	# def loadFile(self,fileName):
		# #Debug("#Open and read a file")
		# print "Opening file '%s' for analyzis" % fileName
		# inFile = open(fileName,'rb')
		# inFileString = inFile.read()
		# self.inFileContents = bytearray(b"%s" % inFileString)
		# self.inFileContentLength = len(self.inFileContents)
		# inFile.close()
		# #Debug("ContentLength: %s bytes" %self.inFileContentLength)
		# pass
	
	

	def avgValue(self,queue):
		sum = 0
		count = 0
		#print "LEngth MA: %s " % queue
		for val in queue:
			if val>-1:
				sum = sum+val
				count = count +1
		try:
			return sum/count
		except:
			return 0
	
	def frameToHuman(self,frame):
		outString = ""
		for byte in frame:
			outString = outString + " " + format(byte, "02X")
		return outString.strip()
		
	def parseLine(self,ba,linenumber):
		#Debug("#parse the passed line")
		#ba = bytearray(b"%s" % line)
		#ba = line
		self.FrameArray[linenumber]=ba
		
		
		if ba[0]==0x7e and ba[1]==0xfe:
			
			if len(ba)!=11:
				newframe = bytearray(b"%s" % ba[0:2])
				xor=0x00
				for byte in ba[2:]:
					if byte!=0x7d:
						newbyte = byte ^ xor
						newframe.append(newbyte)
						xor=0x00
					else:
						xor=0x20
					#print byte
				#print "old frame:\t%s" % self.frameToHuman(ba)
				#print "new frame:\t%s" % self.frameToHuman(newframe)
				ba = newframe
			
			AD1 = ba[2]
			AD2 = ba[3]
			RSSIrx = ba[4]
			RSSItx = ba[5]/2
			
			self.tmpAD1.append(AD1)
			self.tmpAD2.append(AD2)
			
			# add this to a datastorage
			dataHash = {"AD1":self.avgValue(self.tmpAD1),"AD2":self.avgValue(self.tmpAD2),"RSSIrx":RSSIrx,"RSSItx":RSSItx,"linenumber":linenumber}
				
			self.ADArray[linenumber]=dataHash
			self.CurrentADData = dataHash
			return dataHash	
			
		elif ba[0]==0x7E and ba[1]==0xFC:
			print "AD1 Threshold 1"
			print "\t%s" % ba
		elif ba[0]==0x7E and ba[1]==0xFB:
			print "AD1 Threshold 2"
			print "\t%s" % ba
		elif ba[0]==0x7E and ba[1]==0xFA:
			print "AD2 Threshold 1"
			print "\t%s" % ba
		elif ba[0]==0x7E and ba[1]==0xF9:
			print "AD2 Threshold 2"
			print "\t%s" % ba
		elif ba[0]==0x7E and ba[1]==0xFD:
			print "User Data"
			self.UserFrameArray[linenumber]=ba
			print "\t%s" % ba
		else:
			# this line failed to parse for some reason
			# add it to the failStack
			self.UnparsedFrameArray[linenumber]=ba
			
		return False
		
	def setMovingAverageSize(self,count):
		#print count
		if count <1:
			count=1
		self.tmpAD1 = deque([-1]*count,count)
		self.tmpAD2 = deque([-1]*count,count)
		

		
	

class FrSkyLogger:
	def __init__(self,options):
		self.options = options
		self.parser = FrSkyParser(options)
		
		#self.openFiles()
	
	def openRawFile(self,f):
		try:
			self.rawfile = open(f,'wb+')
		except:
			print "could not open '%s'" % f
			
	def openAscFile(self,f):
		try:
			self.ascfile = open(f,'wb+')
		except:
			print "could not open '%s'" % f
			
	def openCsvFile(self,f):
		try:
			print "Writing CSV to: %s" % f
			self.csvfile = open(f,'wb+')
			self.csvfile.write("sample#;AD1;AD2;RSSIrx;RSSItx\n")
		except:
			print "could not open '%s'" % f
			
	def setLoggingPrefix(self,prefix):
		self.loggingPrefix=prefix
		self.openFiles()
			
	def openFiles(self):
		if self.options.csvLogging:
			self.openCsvFile("logs/%s.CSV" % self.loggingPrefix)
		
		if self.options.ascLogging:
			self.openAscFile("logs/%s.ASC" % self.loggingPrefix)
		
		if self.options.rawLogging:
			self.openRawFile("logs/%s.RAW" % self.loggingPrefix)
		#self.parser.setMovingAverageSize(options.movingaverage)
		
	
	def log(self,frame,data):
		if self.options.csvLogging:
			self.writeCsv(data)
		if self.options.ascLogging:
			self.writeAsc(frame)
		if self.options.rawLogging:
			self.writeRaw(frame)
		pass
		
	def writeCsv(self,data):
		"""Write CSV data"""
		try:
			self.csvfile.write("%s;%s;%s;%s;%s\n" % (data["linenumber"],data["AD1"],data["AD2"],data["RSSIrx"],data["RSSItx"]))
		except:
			self.openCsvFile("logs/%s.CSV" % self.loggingPrefix)
			self.csvfile.write("%s;%s;%s;%s;%s\n" % (data["linenumber"],data["AD1"],data["AD2"],data["RSSIrx"],data["RSSItx"]))
			pass
	
	def writeAsc(self,frame):
		"""Write human readable frame"""
		try:
			self.ascfile.write("%s\n" % self.parser.frameToHuman(frame))
		except:
			self.openAscFile("logs/%s.ASC" % self.loggingPrefix)
			self.ascfile.write("%s\n" % self.parser.frameToHuman(frame))
			pass
		
		
	def writeRaw(self,frame):
		"""Write out RAW data"""
		try:
			self.rawfile.write(frame)
		except:
			self.openRawFile("logs/%s.RAW" % self.loggingPrefix)
			self.rawfile.write(frame)
			pass
	
	def stop(self):
		try:
			self.rawfile.close()
		except:
			pass
		try:
			self.csvfile.close()
		except:
			pass
		try:
			self.ascfile.close()
		except:
			pass			


class FrSkyServerX(Frame):
	def __init__(self,options,config,master=None):
		Frame.__init__(self,master)
		self.top = self.winfo_toplevel()
		
		self.helv36 = tkFont.Font ( family="Helvetica",size=36, weight="bold" )
		self.helv72 = tkFont.Font ( family="Helvetica",size=72, weight="bold" )
	
		self.startTime = time.time()
		self.runningTime = 0
		self.config=config
		self.fullscreen=False
		#self.configure(bg='red')
		# read in configuration from file
		self.AD1 = {}
		self.AD2 = {}
		self.AD1["enabled"] = config.getboolean("AD1","enabled")
		#if self.AD1["enabled"]:
		try:
			self.AD1["unit"] = config.get("AD1","unit")
			self.AD1["factor"] = eval(config.get("AD1","factor"))
			self.AD1["offset"] = eval(config.get("AD1","offset"))
			self.AD1["description"] = config.get("AD1","description")
			self.AD1["max"]=255*self.AD1["factor"]+self.AD1["offset"]
		except:
			self.AD1["description"]=""
		
		self.AD2["enabled"] = config.getboolean("AD2","enabled")
		#if self.AD2["enabled"]:
		try:
			self.AD2["unit"] = config.get("AD2","unit")
			self.AD2["factor"] = eval(config.get("AD2","factor"))
			self.AD2["offset"] = eval(config.get("AD2","offset"))
			self.AD2["description"] = config.get("AD2","description")
			self.AD2["max"]=255*self.AD2["factor"]+self.AD2["offset"]
		except:
			self.AD2["description"]=""
			pass
	
		
		self.serial = serial.Serial()

		
		#print "AD1 Config:"
		#print self.AD1
		
		
		self.ctrlvar = {}
		#self.grid(sticky=N+S+E+W)
		#self.grid()
		
		#self.place(x=0, y=0)
		#self.pack()
		
		#wm_protocol(self,"WM_DELETE_WINDOW", self.stop)
		self.bind("<Destroy>",self.stop)
		self.top.bind("<Configure>",self.__resized)
		self.options=options
		self.TotalSampleCount=0
		print "Creating parser"
		self.parser = FrSkyParser(options)
		
		
		self.serialPorts = self.scanSerialPorts()
		
		print "Creating Logger"
		self.logger = FrSkyLogger(options)
		
		self.createWidgets()	
		
		
		self.grid(row=1,column=1,sticky=E+W)
		self.oldGeometry = self.top.geometry()
		self.oldWidth=0
		self.oldHeight=0
		#upon startup, open serial port if -p option given
		if options.port!=None:
			self.openPort(options.port)
		elif options.infile!=None:
			# Move this to menu item
			self.loadFile(options.infile)
			self.parseFile()

			self.printSummary()
		else:
			pass
			
		
			
		
		self.start()
#	def mainloop(self):
#		print "main"
	def __resized(self,event):
		x,y,w,h = event.x,event.y,event.width,event.height
		#print x,y,w,h
		if self.top.wm_state()=="zoomed":
			# Act on fullscreen
			self.fullscreen=True
			
			# disable frame.
			self.top.overrideredirect(1)
			
			
		else:
			# Act on normalize
			self.fullscreen=False
			
			# Enable window frame
			self.top.overrideredirect(0)
		
		ww = self.top.winfo_width()
		hh = self.top.winfo_height()
		
		# any other scaling:
		if ww!=self.oldWidth or hh!=self.oldHeight:
			
			self.oldWidth=ww
			self.oldHeight=hh
			self.widgetWidth = (ww-(6*2))/3
			self.widgetHeight = (hh-50)/2
			
			self.ad1Frame.resize(self.widgetWidth,self.widgetHeight)
			self.ad2Frame.resize(self.widgetWidth,self.widgetHeight)
			self.clockFrame.resize(self.widgetWidth,self.widgetHeight)
			self.infoFrame.resize(self.widgetWidth,self.widgetHeight)

	
	def __toggleFullscreen(self):
		if self.top.wm_state()=="zoomed":
			self.top.wm_state('normal')
		else:
			self.top.wm_state('zoomed')
		#root = Tk()

		# make it cover the entire screen
		# if self.fullscreen:
			# self.fullscreen=False
			# self.top.overrideredirect(0)
			# self.top.geometry(self.oldGeometry)
		# else: #is not fullscreen atm
			
			# w, h = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
			# x,y = self.top.winfo_rootx(), self.top.winfo_rooty()
			# xx,yy = self.top.winfo_x(),self.top.winfo_y()
			# self.top.overrideredirect(1)
			# print "x: %s, Y: %s" % (x,y)
			# print "x: %s, Y: %s" % (xx,yy)
			# self.top.geometry("%dx%d+0+0" % (w, h))
			# self.fullscreen=True
			
		
		

	
	def scanSerialPorts(self):
		"""scan for available ports. return a list of tuples (num, name)"""
		available = []
		for i in range(256):
			try:
				s = serial.Serial(i)
				available.append( (i, s.portstr))
				s.close()   # explicit close 'cause of delayed GC in java
			except serial.SerialException:
				pass
		return available

	
	def openPort(self,port):

		print "Opening port '%s'" % port
		
		
		# stop any running port monitors
		if self.serial.isOpen():
			print "Closing port %s" % self.serial.name
			self.serial.close()
		
		# reset any counters etc
		self.ctrlvar["AD1Volt"].set("NA")
		self.ctrlvar["AD2Volt"].set("NA")
		self.ctrlvar["samples"].set(0)
		self.loggingPrefix = time.strftime("%Y%m%d_%H%M%S", time.localtime())
		self.infoFrame.setLoggingPrefix(self.loggingPrefix)
		self.logger.setLoggingPrefix(self.loggingPrefix)
		

		print "LoggingPrefix: %s" % self.loggingPrefix
		
		# open the port
		try:
			self.serial = serial.Serial(port,timeout=1,writeTimeout=1)
		except serial.serialutil.SerialException:
			print "Could not open serial port '%s'" % port
			
			
	def closePort(self):
		try:
			print "Serial open: %s" % self.serial.isOpen()
			if self.serial.isOpen():
				self.serial.close()
		except:
			pass

	
	
	def createWidgets(self):
		
		courier10 = tkFont.Font ( family="Courier",size=9 )
		
		
#		top = self.winfo_toplevel()
		self.top.columnconfigure(0,weight=1)
		self.top.columnconfigure(6,weight=1)
		self.top.rowconfigure(3,weight=1)
		self.ctrlvar["AD1Volt"] = StringVar()
		self.ctrlvar["AD2Volt"] = StringVar()
		self.ctrlvar["RSSIrx"] = StringVar()
		self.ctrlvar["RSSItx"] = StringVar()
		self.ctrlvar["samples"] = StringVar()
		self.ctrlvar["status"] = StringVar()

		self.rowconfigure(2,weight=1)
		
		self.frameStatus = Label(self.top,text="BAH",textvariable=self.ctrlvar["status"],relief=SUNKEN,bd=1,anchor=W,font=courier10)
		self.frameStatus.grid(row=4,column=0,columnspan=7, sticky="we")
		
		
		#self.framestatus =StatusBar(self)
		
		#self.status = Label(self, text="", bd=1, relief=SUNKEN, anchor=W)
		#self.status.pack(side="bottom", fill="x",expand=1)
		#self.status.grid()
		
			
		#self.clock = Label(self,font=self.helv72)
		#self.clock.grid(row=0,column=3)
		#self.clock.after(1000,self.tick)
		#self.btnResetTimer = Button(self,text='Reset',command=self.resetTimer)
		#self.btnResetTimer.grid(row=1,column=3,sticky=E+W)
		
		
		
		
		self.ad1Frame = AdFrame(self)
		self.ad1Frame.setName("AD1: %s" % self.AD1["description"])
		self.ad1Frame.grid(row=0,column=1)
		self.ad1Frame.setMinMax(0,4.2)
		self.ad1Frame.setUnit(self.AD1["unit"])
		self.ad1Frame.setEnabled(self.AD1["enabled"])

		self.clockFrame = TimeFrame(self)
		self.clockFrame.grid(row=0,column=3)
		
		self.ad2Frame = AdFrame(self)
		self.ad2Frame.setName("AD2: %s" % self.AD2["description"])
		self.ad2Frame.grid(row=0,column=5)
		self.ad2Frame.setMinMax(0,26)
		self.ad2Frame.setUnit(self.AD2["unit"])
		self.ad2Frame.setEnabled(self.AD2["enabled"])

		self.infoFrame = InfoFrame(self,self.options)
		self.infoFrame.grid(row=1,column=1)
		
		#top.rowconfigure(0, weight=1)
		#top.columnconfigure(0, weight=1)
		#top.columnconfigure(6, weight=1)

		
		#self.ad1Frame.setProgress(30)
		
		self.setStatus(0,0,0,0,0)
		
		
		# MENUS 
		self.menuBar = Menu(self.top)
		self.top["menu"] = self.menuBar

		self.fileMenu = Menu(self.menuBar)
		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		#self.fileMenu.add_command(label="Open Port", command=self.__fileOpenPort)
		self.serialPortMenu = Menu(self.menuBar)
		#print self.serialPorts
		for p in self.serialPorts:
			#print p[1]
			self.serialPortMenu.add_command(label=p[1],command=lambda: self.__fileOpenPort(p[1]))
		
		
		self.fileMenu.add_cascade(label="Open Serial Port",menu=self.serialPortMenu)
		
		self.fileMenu.add_command(label="Close Port", command=self.__fileClosePort)
		self.fileMenu.add_command(label="Open LogFile", command=self.__fileOpenLogFile)
		self.fileMenu.add_command(label="Export LogFile", command=self.__fileExportLogFile)
		self.fileMenu.add_command(label="Export Human Readable File", command=self.__fileExportHumanFile)
		self.fileMenu.add_command(label="Export CSV File", command=self.__fileExportCsvFile)
		self.fileMenu.add_command(label="Fullscreen",command=self.__toggleFullscreen)
		self.fileMenu.add_command(label="Quit", command=self.__fileQuitHandler)
		
		self.helpMenu = Menu(self.menuBar)
		self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
		self.helpMenu.add_command(label="About", command=self.__aboutHandler)
		
		
	
	def resetTimer(self):
		self.startTime=time.time()
		self.runningTime = 0
		minutes = int(self.runningTime/60)
		secs = "%s" % int(self.runningTime-(minutes*60))
		
		minSec = "{:0>2}:{:0>2}".format(minutes,secs)
		self.clock.config(text="%s" % minSec)
	
	
		
		
	def __aboutHandler(self):
		print "FrSky Dashboard by Espen Solbu"
		pass
		
	def __fileOpenPort(self,port=None):
		# open dialog to choose comport
		print "trying to open %s" % port
		self.openPort(port)
		pass
		
	def __fileClosePort(self):
		self.closePort()
		pass
	
	def __fileOpenLogFile(self):
		pass
	
	def __fileExportLogFile(self):
		pass
	def __fileExportHumanFile(self):
		pass
	def __fileExportCsvFile(self):
		pass
		
	def __fileQuitHandler(self):
		# Destroy the main frame, this will raise the destroy event, that closes all threads and exits
		self.destroy()
		
		
	def printSummary(self):
		#Debug("#echo out a summary")
		print ""
		sys.stdout.write(" Summary ".center(80,"="))
		seconds1 = self.TotalSampleCount/30
		minutes = seconds1/60
		seconds = seconds1-(minutes*60)
		print "Number of samples: %s (%s minutes, %s seconds)" % (self.TotalSampleCount,minutes,seconds)
		print "Frames used for moving average: %s" % len(self.parser.tmpAD1)
		### TODO: FIX below
		#print "Unparseable samples: %s" % len(self.UnparsedFrameArray)
		#print "\tLine#\tData"
		#for linenumber,line in self.UnparsedFrameArray.items():
		#	print "\t%s:\t%s" % (linenumber,self.frameToHuman(line))
		pass
		
	def parseFile(self):
		self.startTime = time.time()
		
		print "Parsing %s bytes of data, please wait..." % self.inFileContentLength
		
		self.ADArray = {}
		self.CurrentADData = {}
	

		#self.tmpAD1dev = 0
		#self.tmpAD2dev = 0
	
		
		
		
		
		position = 0
		linecount = 0
		blocksShowing = 0
		currentLine = ""
		currentFrame = ""
		self.progress = 0
		frameLength=0
		frameStart=0
		self.TotalSampleCount=0
		
		for val in self.inFileContents:
			position = position + 1
			currentByte = val
			frameLength = frameLength+1

			# do we have a full frame?
			if currentByte==0x7e and frameLength>3:
				currentFrame = self.inFileContents[frameStart:frameStart+frameLength]
				
				frameData = self.parser.parseLine(currentFrame,linecount)
				#print frameData
				self.TotalSampleCount = self.TotalSampleCount + 1
				if frameData:
					self.logger.log(currentFrame,frameData)
				linecount += 1
				currentFrame = ""
				frameLength=0
				frameStart=position
				self.progress = position*100/self.inFileContentLength
				blocksToShow = self.progress*80/100
				while blocksShowing<blocksToShow:
					sys.stdout.write("#")
					blocksShowing = blocksShowing+1
		
		self.endTime = time.time()
		self.parseTime = self.endTime-self.startTime
		
		print "Parsing complete in %s s" % self.parseTime
		pass
	
	def loadFile(self,fileName):
		print "Opening file '%s' for analyzis" % fileName
		inFile = open(fileName,'rb')
		inFileString = inFile.read()
		self.inFileContents = bytearray(b"%s" % inFileString)
		self.inFileContentLength = len(self.inFileContents)
		inFile.close()
		#Debug("ContentLength: %s bytes" %self.inFileContentLength)
		pass
			
	def start(self):
		if self.serial!=None:
			self.alive = True
			# start serial->console thread
			self.receiver_thread = threading.Thread(target=self.reader,name="Serial Reader Thread")
			self.receiver_thread.setDaemon(1)
			self.receiver_thread.start()
			# enter console->serial loop
			self.transmitter_thread = threading.Thread(target=self.writer,name="Serial Writer Thread")
			self.transmitter_thread.setDaemon(1)
			self.transmitter_thread.start()
			# enter keyboard reader loop
			#self.keyboard_thread = threading.Thread(target=self.keyboardreader)
			#self.keyboard_thread.setDaemon(1)
			#self.keyboard_thread.start()
			self.startTime = time.time()
			self.runningTime = 0

	def stop(self,event=None):
		print "User desided to quit. Coward"
		
		self.printSummary()
		print "Waiting for all threads to end"
		self.alive = False
		while len(threading.enumerate())>1:
			time.sleep(0.1)
				
		#time.sleep(2)
		
		#print "Attemting quit()"
		self.quit()
		
		# exit(0) seems to work...
		#print "Attempting exit(0)"
		exit(0)
		#print "Attempting sys,exit(0)"
		#sys.exit(0)
		

	def join(self, transmit_only=False):
		if self.serial!=None:
			self.transmitter_thread.join()
			#if not transmit_only:
			self.receiver_thread.join()	
			#self.keyboard_thread.join()	
	
	def writer(self):
		while self.alive:
			time.sleep(0.1)
			pass
		print "Stopping Writer thread"
	
	def keyboardreader(self):
		# read keyboard to allow exit
		
		while self.alive:
			try:
				c = msvcrt.getch()
				if c==chr(27):
					self.alive=False
					print "Escape pressed"
					#sys.exit(0)
				elif c==chr(3):
					self.alive=False
					print "Ctrl-C pressed"
					#sys.exit(0)
				else:
					print "'%s'" % ord(c)
			except SystemExit:
				print "Exiting FrSky Dashboard (systemexit)"
				
			except KeyboardInterrupt:
				c = '\x03'
				print "key pressed?"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				raise
				print "no key pressed"
		
		
		print "Exiting FrSky Dashboard"
		self.printSummary()
		# if self.options.outfile!=None:
			# self.parser.exportCSV(self.options.outfile)
		# if self.options.framefile!=None:
			# self.parser.exportHumanFrames(self.options.framefile)
		#sys.exit(0)
		print "Stopping Keyboard thread"
	
	def setStatus(self,ad1,ad2,RSSIrx,RSSItx,linenumber):
		statusstr = "{:<11}{:<11}{:<14}{:<14}{:>30}".format("AD1: %s" % ad1,"AD2: %s" % ad2,"RSSIrx: %s" % RSSIrx,"RSSItx: %s" % RSSItx,"#Samples: %s" % linenumber)
		#print statusstr
		#statusstr = "AD1: %s\t\tAD2: %s\t\tRSSIrx: %s\t\tRSSItx: %s\t\t#Samples: %s\t\t" % (ad1,ad2,RSSIrx,RSSItx,linenumber) 
		self.ctrlvar["status"].set(statusstr)
	
	def reader(self):
		"""loop and copy serial->console"""
		currentFrame = bytearray(b"")
		frameLength=0
		frameCount=0
		
		while self.alive:
			if self.serial.isOpen():
				try:
					data = self.serial.read(1)
				except:
					data = ""
				if len(data)>0:
					currentByte = ord(data)
					if frameLength>100:
						exit(1)
					elif currentByte==0x7e and frameLength>4:
						currentFrame.append(currentByte)
						#print self.parser.frameToHuman(currentFrame)
						#sys.stdout.write('.')
						
						frameData = self.parser.parseLine(currentFrame,frameCount)
						#print frameData
						self.TotalSampleCount = self.TotalSampleCount + 1
						if frameData:
							self.logger.log(currentFrame,frameData)
							#self.ctrlvar["AD1"].set(frameData["AD1"])
							#self.ctrlvar["AD2"].set(frameData["AD2"])
							self.ctrlvar["RSSIrx"].set(frameData["RSSIrx"])
							self.ctrlvar["RSSItx"].set(frameData["RSSItx"])
							self.ctrlvar["samples"].set(frameData["linenumber"])
							
							#if self.AD1["enabled"]==True:
							if self.ad1Frame.enabled==True:
								ad1V = (frameData["AD1"]*self.AD1["factor"])+self.AD1["offset"]
								self.ctrlvar["AD1Volt"].set("%.2f%s" % (ad1V,self.AD1["unit"]))
								try:
									self.ad1Frame.setValue(ad1V)
								except:
									pass
							#if self.AD2["enabled"]==True:
							if self.ad2Frame.enabled==True:
								ad2V = (frameData["AD2"]*self.AD2["factor"])+self.AD2["offset"]
								self.ctrlvar["AD2Volt"].set("%.2f%s" % (ad2V,self.AD2["unit"]))
								try:
									self.ad2Frame.setValue(ad2V)
								except:
									pass

							#self.currentTime = time.time()
							#self.runningTime = self.currentTime-self.startTime
							#self.clockFrame.runningTime=self.runningTime
							self.clockFrame.update()
							#print self.runningTime
							
							
							self.setStatus(frameData["AD1"],frameData["AD2"],frameData["RSSIrx"],frameData["RSSItx"],frameData["linenumber"])
							
						currentFrame=bytearray(b"")
						frameCount=frameCount+1
						frameLength=0
					else:
						currentFrame.append(currentByte)
						frameLength = frameLength+1
			else:
				frameCount=0
				time.sleep(0.1)
		print "Stopping Reader thread"
		
