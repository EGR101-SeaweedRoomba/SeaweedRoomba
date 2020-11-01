from sense_hat import SenseHat
import socket
import time
import struct
sense = SenseHat()

sense. show_message("Let's gooooo!")
sense.load_image('Arrow.png')
PORT = 65432 # The server's hostname or IP address
HOST = '10.197.12.245'        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		orientation = sense.get_gyroscope()
		#print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
		b1 = struct.pack("i", int(orientation['yaw']))
		#print(int(orientation['pitch']))
		print(str(b1))
		s.send(b1 + b'EE')
		time.sleep(0.1)






