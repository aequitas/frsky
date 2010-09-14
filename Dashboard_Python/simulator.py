import serial,os,sys,threading,msvcrt,time

from optparse import OptionParser

class FrSkySimulator:
	def __init__(self,opts):
		self.options=opts
		try:
			self.serial = serial.serial_for_url(self.options.port,timeout=1,writeTimeout=1)
		except AttributeError:
			# happens when the installed pyserial is older than 2.5. use the
			# Serial class directly then.
			self.serial = serial.Serial(self.options.port,timeout=1)
		self.AD1=0
		self.AD2=0
		self.RSSIrx=90
		self.RSSItx=90
	def start(self):
		self.alive = True
		# start serial->console thread
		self.receiver_thread = threading.Thread(target=self.reader)
		self.receiver_thread.setDaemon(1)
		self.receiver_thread.start()
		# enter console->serial loop
		self.transmitter_thread = threading.Thread(target=self.writer)
		self.transmitter_thread.setDaemon(1)
		self.transmitter_thread.start()
		# enter keyboard reader loop
		self.keyboard_thread = threading.Thread(target=self.keyboardreader)
		self.keyboard_thread.setDaemon(1)
		self.keyboard_thread.start()
		print "Simulator started"
		print "press Ctrl-C to abort"
		

	def stop(self):
		self.alive = False

	def join(self, transmit_only=False):
		self.transmitter_thread.join()
		self.receiver_thread.join()	
		self.keyboard_thread.join()
	
	def writer(self):
		#write data to serial port
		
		while self.alive:
			self.AD1 = self.AD1+1
			self.AD2 = self.AD2-1
			if self.AD1>254:
				self.AD1=0
			if self.AD2<0:
				self.AD2=254
			outString = "\x7e\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x7e"
			outba = bytearray(b"%s" % outString)
			outba[2]=self.AD1
			outba[3]=self.AD2
			outba[4]=self.RSSIrx
			outba[5]=self.RSSItx*2
			# apply bytestuffing routine
			outba2 = bytearray(b"")
			n=0
			for byte in outba:
				if n>1 and n<len(outba)-1:
					if byte==0x7e:
						outba2.append(0x7d)
						outba2.append(0x5e)
					elif byte==0x7d:
						outba2.append(0x7d)
						outba2.append(0x5d)
					else:
						outba2.append(byte)
				else:
					outba2.append(byte)
				n = n+1
			
			#sys.stdout.write("IN: ")
			#for byte in outba:
			#	sys.stdout.write(hex(byte)+",")
			#sys.stdout.write("\n")
			
			#sys.stdout.write("OUT: ")
			#for byte in outba2:
			#	sys.stdout.write(hex(byte)+",")
			#sys.stdout.write("\n")
			try:
				self.serial.write(outba2)
			except:
				pass
			time.sleep(0.03)
			
		self.alive=False
		print "Stopping writer thread"
	
	def reader(self):
		# read data from serial port"
		while self.alive:
			try:
				#pass
				char = self.serial.read(1)
				#print char
					
					
			except serial.SerialException, e:
				self.alive = False
				# would be nice if the console reader could be interruptted at this
				# point...
				raise
		self.alive=False
		print "Stopping reader thread"
	
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
				print "Exiting simulator"
				self.alive=False
			except KeyboardInterrupt:
				c = '\x03'
				print "key pressed?"
			except:
				print "Unexpected error:", sys.exc_info()[0]
				raise
				print "no key pressed"
		print "EXIT"
		self.alive=False
		return False


op = OptionParser()
op.add_option("-p","--port",dest="port",
	help="write simulatordata to COMPORT", metavar="COMPORT", default="COM8")
(options,args) = op.parse_args()



simulator = FrSkySimulator(options)
simulator.start()
simulator.join()
	

