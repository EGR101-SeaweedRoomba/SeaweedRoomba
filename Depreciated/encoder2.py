import RPi.GPIO as GPIO
from time import sleep

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

def aiA(channel):
      global counter1
      if GPIO.input(dt1):
                counter1 -=1
      else:
                counter1 += 1
      return(counter1)

def aiB(channel):
      global counter2
      if GPIO.input(dt2):
                counter2 -=1
      else:
                counter2 +=1
      return(counter2)

GPIO.add_event_detect(clk1, GPIO.RISING, callback=aiA)
GPIO.add_event_detect(clk2, GPIO.RISING, callback=aiB)

try:
      GPIO.wait_for_edge(24, GPIO.RISING)
except:
      GPIO.cleanup()


def getCounterValues():
  return([counter1, counter2])