import time
import board
import busio
import adafruit_bno055
import numpy as np 

 
# Use these lines for I2C
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)
 
# User these lines for UART
# uart = busio.UART(board.TX, board.RX)
# sensor = adafruit_bno055.BNO055_UART(uart)
 
while True:
#    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print(sensor.euler)
    print("Gyro: {}".format([max(0,int(i or 0)) for i in sensor.euler]))
#    print(90-np.arctan2(sensor.magnetic[1], sensor.magnetic[0])*180/np.pi)
    time.sleep(0.1)
