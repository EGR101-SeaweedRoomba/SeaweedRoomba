import socket
import struct
import pygame
import math

HOST = '10.197.12.245'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

screen = pygame.display.set_mode((800,600))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            pygame.event.get()
            data = conn.recv(1024)
            if data:
                #print(str(data))
                for val in data.split(b'\x00EE'):
                    
                    if val:
                        screen.fill((0,0,0
                                     ))
                        print(str(val+(4-len(val))*b'\x00'))
                        angle = struct.unpack("i", val+(4-len(val))*b'\x00')[0]
                        print(angle)
                        pygame.draw.line(screen, (255, 255, 255), (400,300)
                                         , (400+120*math.cos(math.radians(angle)),
                                            300+120*math.sin(math.radians(angle))))
                        pygame.display.flip()
