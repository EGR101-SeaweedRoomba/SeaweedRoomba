import json
import threading
import time
import random
import RPi.GPIO as GPIO
import math
import flask
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

interval=0.1

x=0
y=0
theta = 0
wheelbase = 0.47
radius = 0.0889
gearratio =44/92

counters = {
    "c1":0,
    "c1_":0,
    "c2":0,
    "c2_":0,
}

# Create flask application.
app = flask.Flask(__name__)

data = {}

def aiA(channel):
    if GPIO.input(dt1):
        counters["c1"] +=1
    else:
        counters["c1"] -= 1

def aiB(channel):
    if GPIO.input(dt2):
        counters["c2"] -=1
    else:
        counters["c2"] += 1



def calculate(vel1, vel2):
    global x, y, theta

    # deltat = 0.1

    # vl = (vel1+vel2)/2
    # vr = (vel1-vel2)/wheelbase

    # k00 = vl*math.cos(theta)
    # k01 = vl*math.sin(theta)
    # k02 = vr

    # k10 = vl*math.cos(theta+deltat/2*k02)
    # k11 = vl*math.sin(theta+deltat/2*k02)
    # k12 = vr

    # k20 = vl * math.cos(theta + deltat*k12/2)
    # k21 = vl* math.sin(theta + deltat*k12/2)
    # k22 = vr

    # k30 = vl * math.cos(theta + deltat*k22) 
    # k31 = vl * math.sin(theta + deltat*k22) 
    # k32 = vr

    # x += (deltat)/6 * (k00+2*(k10+k20)+k30)
    # y += (deltat/6)*(k01+2*(k11+k21)+k31)
    # theta += (deltat/6)*(k02 + 2*(k12+k22) + k32)
    ACCEL_VEL_TRANSITION =  (10) / 1000.0;
    ACCEL_POS_TRANSITION = 0.5 * ACCEL_VEL_TRANSITION * ACCEL_VEL_TRANSITION;
    DEG_2_RAD = 0.01745329251;
    accel = sensor.linear_acceleration
    orient = sensor.euler


    x += ACCEL_POS_TRANSITION*(accel[0] if accel[0] !=None else 0)
    y += ACCEL_POS_TRANSITION*(accel[1] if accel[1] !=None else 0)

    headingVel = ACCEL_VEL_TRANSITION * (accel[0] if accel[0] !=None else 0)/ math.cos(DEG_2_RAD * (orient[0] if accel[0] != None else 0)

    theta = orient[0]
    data['x']=x
    data['y']=y
    data['theta']=theta

def startCalculating():
    """Function to handle sending sensor data to the client web browser
    using HTML5 server sent events (aka server push).  This is a generator function
    that flask will run in a thread and call to get new data that is pushed to
    the client web page.
    """

    ticker = threading.Event()
 
    while not ticker.wait(0.1):
        vel1 = (counters["c1_"]-counters["c1"])/interval
        vel2 = (counters["c2_"]-counters["c2"])/interval

        counters["c1_"]=counters["c1"]
        counters["c2_"]=counters["c2"]

        fac = radius*2*math.pi/600/gearratio

        vel1 *= fac
        vel2 *= fac

        calculate(vel1, vel2)	
        yield "data: {0}\n\n".format(json.dumps(data))

@app.route("/val")
def path():
    # Return SSE response and call sse function to stream sensor data to
    # the webpage.
    print("sending data....")
    return flask.Response(startCalculating(), mimetype="text/event-stream")

@app.route("/")
def root():
    return flask.render_template("index.html")


if __name__ == "__main__":
    # Create a server listening for external connections on the default
    # port 5000.  Enable debug mode for better error messages and live
    # reloading of the server on changes.  Also make the server threaded
    # so multiple connections can be processed at once (very important
    # for using server sent events).
    GPIO.add_event_detect(clk1, GPIO.RISING, callback=aiA)
    GPIO.add_event_detect(clk2, GPIO.RISING, callback=aiB)

    app.run(host="0.0.0.0", debug=True, threaded=True)