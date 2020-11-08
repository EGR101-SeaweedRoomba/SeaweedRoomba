import RPi.GPIO as GPIO
import time
import math
import board
import busio
import adafruit_bno055

clk1 = 27
dt1 = 4

clk2 = 26
dt2 = 6

GPIO.setmode(GPIO.BCM)

GPIO.setup(clk1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

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
    global counter1
    global old1
    global oldtime1
    global vel1

    if GPIO.input(dt1):
        counter1 +=1
    else:
        counter1 -= 1

    if (abs(counter1-old1)>=4):
        accel = math.sqrt(sum(val**2 for val in sensor.acceleration))
        print("Accel 1: " + str(accel))
        if accel > 0.1:
            vel1 = round(radius*2*math.pi/600*(counter1-old1)/(time.time()-oldtime1)/gearratio,2)
        else:
            vel1 = 0
            vel2 =0
        calculate()
        old1=counter1
        oldtime1=time.time()
  
def aiB(channel):
    global counter2
    global old2
    global oldtime2
    global vel2

    if GPIO.input(dt2):
        counter2 +=1
    else:
        counter2 -= 1

    if (abs(counter2-old2)>=4):
        accel = math.sqrt(sum(val**2 for val in sensor.acceleration))
        #print("Accel 2: " + str(accel))
        if accel > 0.1:
            vel2 = round(radius*2*math.pi/600*(counter2-old2)/(time.time()-oldtime2)/gearratio,2)
        else:
            vel1=0
            vel2=0
        calculate()
        old2=counter2	
        oldtime2=time.time()

def calculate():

    global time0
    global theta
    global x
    global y
    global vel1
    global vel2

    deltat = time.time()-time0

    vl = (vel1+vel2)/2
    vr = (vel1-vel2)/wheelbase

    k00 = vl*math.cos(theta)
    k01 = vl*math.sin(theta)
    k02 = vr

    k10 = vl*math.cos(theta+deltat/2*k02)
    k11 = vl*math.sin(theta+deltat/2*k02)
    k12 = vr

    k20 = vl * math.cos(theta + deltat*k12/2)
    k21 = vl* math.sin(theta + deltat*k12/2)
    k22 = vr

    k30 = vl * math.cos(theta + deltat*k22) 
    k31 = vl * math.sin(theta + deltat*k22) 
    k32 = vr

    x += (deltat)/6 * (k00+2*(k10+k20)+k30)
    y += (deltat/6)*(k01+2*(k11+k21)+k31)
    theta += (deltat/6)*(k02 + 2*(k12+k22) + k32)
    
    time0 = time.time()

#    print(str(vel1) + "   " + str(vel2))
    #print("X: " + str(x) + "\nY: " + str(y) + "\nTheta: " + str(theta*360/(2*math.pi)))

GPIO.add_event_detect(clk1, GPIO.RISING, callback=aiA)
GPIO.add_event_detect(clk2, GPIO.RISING, callback=aiB)

try:
    GPIO.wait_for_edge(24, GPIO.RISING)
except:
    GPIO.cleanup()
