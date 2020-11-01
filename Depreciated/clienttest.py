import socket
import time
import struct

PORT = 65432 # The server's hostname or IP address
HOST = '10.197.12.245'        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
                orientation = sense.get_gyroscope()
                print("p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

                b1 = struct.pack("i", 1)
                b2 = struct.pack("i", 2)
                b3 = struct.pack("i", 3)


                s.send(b'FFFF')
                
                s.send(b1 + b'EEEE')
                s.send(b2 + b'EEEE')
                s.send(b3 + b'EEEE')
                

                time.sleep(0.1)
