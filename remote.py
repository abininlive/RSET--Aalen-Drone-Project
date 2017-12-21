import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)
#ser.close()
x = bytearray(21)
while(True):
	#ser.open()
	#ser.reset_input_buffer()
	while(True):
		ser.readinto(x)
		if(x[0] != 168):  #0xa8
			continue
		else:
			print "NEW"
			print (x[3]<<8|x[4])/8
			print (x[5]<<8|x[6])/8
			print (x[7]<<8|x[8])/8
			print (x[9]<<8|x[10])/8
			break
	#ser.close()
	time.sleep(0.1)
ser.close()
