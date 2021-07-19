~~ Roomba Positioning Program ~~

This is a program designed to run on a raspberry pi computer, onboard a seafloor seaweed roomba. 
With the raspberry pi connected to two rotary encoders, this system will allow a user to view the pi's path on the sea floor in a web browser.

Setup instructions:

- Install a headless Raspbian image onto any Raspberry Pi
- Connected to the raspberry pi, install necessary python libraries listed at the beginning of WebPage/server.py:

  pip install Flask
  
  for IMU integration (unstable):
  pip install Adafruit_BNO055
 
 - Set SeaweedRoomba/WebPage/server.py to run every time the roomba is restarted 
        (e.g. by adding "python SeaweedRoomba/WebPage/server.py" to /etc/rc.local)
 - Connect rotary encoders to the raspberry pi, using ports 27 and 4, and 26 and 6. 
 - Connect rotary encoders to the wheels, noting the gear ratio. 
  - I believe that msot optical square-wave style rotary encoders will work for this. 
        example: https://www.amazon.com/Incremental-Optical-Rotary-Encoder-Collector/dp/B07SKJ1WXB
 - Enter the wheel radius + gear ratio into server.py. 
 - Once the code is running, connect the raspberry pi to any computer using an ethernet cable.
    - to view the UI, type the IP address of the raspberry pi into any web browser on the connected computer 
    (this ip address should be displayed on the raspberry pi when the code runs)
 
 --------
 NOTES
--------

server-w-imu integrates an inertial measurement (incl. accelerometer, gyroscope, magnetometer) but has a tendency to accumulate error more than server.py.

![Setup Schematic](https://github.com/EGR101-SeaweedRoomba/SeaweedRoomba/blob/main/Roomba%20Navigation%20Setup%20(low%20res).png)
