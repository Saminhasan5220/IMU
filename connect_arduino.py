from serial import*
import sys
Port = "/dev/ttyACM0"
Baudrate = 115200
board = Serial(Port,Baudrate)
msg = ""
while msg.find("Arduino ready") == -1:
	while board.inWaiting() == 0:
		pass
	msg = board.readline().decode('utf-8')
print("Connected")
board.flush()
while True:
	try:
		msg = '0' + '\n'
		msg = msg.encode('utf-8')
		board.write(msg)
		while(board.inWaiting()==0): # Wait here untill there is data on the Serial Port
			pass                          # Do nothing, just loop until data arrives
		data = board.readline().decode('utf-8').split(',')
		data[len(data) - 1] = data[len(data) - 1].rstrip()
		print(data)
	except KeyboardInterrupt:
		board.close()

		sys.exit()
