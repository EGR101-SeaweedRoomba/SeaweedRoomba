import socket
import struct
import pygame
import math

HOST = '10.197.12.245'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


screen = pygame.display.set_mode((800,600))

white = (255, 255, 255)
black = (0,0,0)
pos = (400, 300)

pygame.init()

font = pygame.font.SysFont('Arial', 32)

ptext = font.render('Pitch', True, white, black)
ptextRect = ptext.get_rect()
ptextRect.center = (300, 200)

rtext = font.render('Roll', True, white, black)
rtextRect = rtext.get_rect()
rtextRect.center = (400, 200)

ytext = font.render('Yaw', True, white, black)
ytextRect = ytext.get_rect() 
ytextRect.center = (500, 200)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        #print('Connected by', addr)

        prevx=[1,2,3,4,5,6,7,8]
        prevy=[1,2,3,4,5,6,7,8]
        prevz=[1,2,3,4,5,6,7,8]

        xfac=0
        yfac=0
        zfac=0
        
        while True:



            screen.fill((0,0,0))         
            pygame.event.get()
            data = conn.recv(1024)

            pygame.draw.circle(screen, (255,255,255), (300,300), 50, 1)
            pygame.draw.circle(screen, (255,255,255), (400,300), 50, 1)
            pygame.draw.circle(screen, (255,255,255), (500,300), 50, 1)

            screen.blit(ptext, ptextRect)
            screen.blit(rtext, rtextRect)
            screen.blit(ytext, ytextRect)


            
            if data and data != b'GOOBER' and data.find(b'GOO')==-1:
                
                vals = data.decode()

                pitch=vals[0:3]
                roll=vals[3:6]
                yaw=vals[6:9]

                x=int(vals[9:12])-xfac
                y=int(vals[12:15])-yfac
                z=int(vals[15:18])-zfac

                print("Z FACTOR: " + str(zfac))

                compass=vals[18:21]

                del prevx[0]; del prevy[0]; del prevz[0]
                prevx.append(x); prevy.append(y); prevz.append(z)

                if all(abs(el-prevx[0])<=1 and prevx[0]!=0 for el in prevx): xfac=int(vals[9:12])
                if all(abs(el-prevy[0])<=1 and prevy[0]!=0 for el in prevy): yfac=int(vals[12:15])
                if all(abs(el-prevz[0])<=1 and prevz[0]!=0  for el in prevz): zfac=int(vals[15:18])                        
                
                print("Pitch: " + pitch + " Roll: "
                      + roll + " Yaw: " + yaw + "\nX: "
                      + str(x) + " Y: " + str(y) + " Z: " + str(z)
                      + "\nCompass: " + compass)



                pygame.draw.line(screen, (255, 255, 255), (300,300)
                                         , (300+50*math.cos(math.radians(int(pitch))),
                                            300+50*math.sin(math.radians(int(pitch)))))
                pygame.draw.line(screen, (255, 255, 255), (400,300)
                                        , (400+50*math.cos(math.radians(int(roll))),
                                           300+50*math.sin(math.radians(int(roll)))))
                pygame.draw.line(screen, (255, 255, 255), (500,300)
                                        , (500+50*math.cos(math.radians(int(yaw))),
                                           300+50*math.sin(math.radians(int(yaw)))))


                pygame.display.flip()
