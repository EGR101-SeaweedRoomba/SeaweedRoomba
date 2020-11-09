import RPi.GPIO as GPIO
import time
import math

clk1 = 27
dt1 = 4

clk2 = 26
dt2 = 6

GPIO.setmode(GPIO.BCM)

GPIO.setup(clk1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter1=0
counter2=0

oldtime1 = time.time() # time at start in seconds
oldtime2 = time.time()

old1 =0
old2 =0

x=0
y=0
theta=0

# constants defined by the robot (metric units)
radius = 1
gearratio = 1
wheelbase = 1

vel1=0
vel2=0

time0=time.time()





def aiA(channel):

    if GPIO.input(dt1):
        counter1 +=1
    else:
        counter1 -= 1

def aiB(channel):

    if GPIO.input(dt2):
        counter2 +=1
    else:
        counter2 -= 1

GPIO.add_event_detect(clk1, GPIO.RISING, callback=aiA)
GPIO.add_event_detect(clk2, GPIO.RISING, callback=aiB)

try:
    GPIO.wait_for_edge(24, GPIO.RISING)
except:
    GPIO.cleanup()
