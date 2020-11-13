import RPi.GPIO as GPIO
import time

# GPIO pins for encoder 1

clk1 = 27
dt1 = 4

# assigned GPIO pins for second encoder
clk2 = 26
dt2 = 6

gearRatio = 6.0;
radius = 0.622 # wheel radius in meters

GPIO.setmode(GPIO.BCM) # broadcom pinout as opposed to board

# establish data pins as inputs

GPIO.setup(clk1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# kill pin

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialize counter values

counter1=0
counter2=0

# encoder 1 callback 

vals1=[0]*20
vals2=[0]*20

def aiA(channel):
       global counter1
       if GPIO.input(dt1):
                counter1 -=1
       else:
                counter1 += 1
       print(counter1*0.6)

# encoder 2 callback

def aiB(channel):
       global counter2
       if GPIO.input(dt2):
                counter2 -=1
       else:
                counter2 +=1

# make data pins responsive to input

GPIO.add_event_detect(clk1, GPIO.RISING, callback=aiA)
GPIO.add_event_detect(clk2, GPIO.RISING, callback=aiB)


# basically just an infinite loop



While(True):
       vals1=vals1[1:]+[counter1]
       vals2=vals2[1:]+[counter2]

       vel1 = sum(vals1)/len(vals1)
       vel2 = sum(vals2)/len(vals2)
       
