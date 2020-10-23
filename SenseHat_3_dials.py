
from sense_hat import SenseHat 
import socket 
import time 
import struct

PORT = 65432 # The server's hostname or IP address
HOST = '10.197.12.245'        # The port used by the server

sense = SenseHat()

orientation = sense.get_gyroscope()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
                orientation = sense.get_gyroscope()
                accel = sense.get_accelerometer_raw()

                print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
                compass = sense.get_compass()

                b1 = str(int(orientation['pitch'])).zfill(3).encode()
                b2 = str(int(orientation['roll'])).zfill(3).encode()
                b3 = str(int(orientation['yaw'])).zfill(3).encode()

                b4 = str(int(accel['x']*100)).zfill(3).encode()
                b5 = str(int(accel['y']*100)).zfill(3).encode()
                b6 = str(int(accel['z']*100)).zfill(3).encode()

                b7 = str(compass).zfill(3).encode()

                s.sendall(b1+b2+b3+b4+b5+b6+b7)
#                s.sendall(b2)
#                s.sendall(b3)
		
                s.sendall(b'GOOBER')                

                time.sleep(0.1)

