import RPi.GPIO as GPIO
from time import sleep

clk1 = 27
dt1 = 4

clk2 = 17
dt2 = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(clk1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


counter1 = 0
counter2 = 0
clkLastState1 = GPIO.input(clk1)
clkLastState2 = GPIO.input(clk2)

try:

        while True:
                clkState1 = GPIO.input(clk1)
                dtState1 = GPIO.input(dt1)
                if clkState1 != clkLastState1:
                        if dtState1 != clkState1:
                                counter1 += 1
                        else:
                                counter1 -= 1
                        print(counter1)

                clkState2 = GPIO.input(clk2)
                dtState2 = GPIO.input(dt2)
                if clkState2 != clkLastState2:
                        if dtState2 != clkState2:
                                counter2 += 1
                        else:
                                counter2 -= 1
                        print(counter2)

                clkLastState1 = clkState1
                clkLastState2 = clkState2

             
finally:
        GPIO.cleanup()
