import RPi.GPIO as GPIO
import time
import math
import threading

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

interval=0.1

x=0
y=0
theta=0

wheelbase =1
radius =1
gearratio =1

counters = {
    "c1":0,
    "c1_":0,
    "c2":0,
    "c2_":0,
}

def aiA(channel):
    if GPIO.input(dt1):
        counters["c1"] +=1
    else:
        counters["c1"] -= 1

def aiB(channel):
    if GPIO.input(dt2):
        counters["c2"] +=1
    else:
        counters["c2"] -= 1


def calculate(vel1, vel2):

    global x, y, theta

    deltat = 0.1

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
    
    print("X: " + str(x) + "    Y: " + str(y) + "     Theta: " + str(theta*180/math.pi))

def startCalculating():
    threading.Timer(interval, startCalculating).start()

    vel1 = (counters["c1_"]-counters["c1"])/interval
    vel2 = (counters["c2_"]-counters["c2"])/interval

    counters["c1_"]=counters["c1"]
    counters["c2_"]=counters["c2"]

    fac = radius*2*math.pi/600/gearratio

    vel1 *= fac
    vel2 *= fac

    calculate(vel1, vel2)

GPIO.add_event_detect(clk1, GPIO.RISING, callback=aiA)
GPIO.add_event_detect(clk2, GPIO.RISING, callback=aiB)

startCalculating()
