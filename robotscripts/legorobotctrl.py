#!/usr/bin/env python3

print('Starting up...')
print('Loading EV3 dependencies...')
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveSteering, MoveDifferential, MoveTank
from ev3dev2.wheel import EV3Tire
from ev3dev2.button import Button
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import InfraredSensor, TouchSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply

steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
STUD_MM = 8
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3Tire, 16 * STUD_MM)
steering_drive.on(0, SpeedPercent(0))
print('Motors initialized')

print('Loading ROS and other dependencies...')
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import json
from time import sleep
from math import degrees
import threading
import datetime
from random import uniform

class EV3DEV(object):

    direction = "stop"

    def __init__(self):
        self.exit = True
        self.callback_exit = True
        # Connect sensors and buttons.
        self.btn = Button()
        #self.ir = InfraredSensor()
        self.ts = TouchSensor()
        self.power = PowerSupply()
        self.tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
        print('EV3 Node init starting')
        rospy.init_node('ev3_robot', anonymous=True, log_level=rospy.DEBUG)
        print('EV3 Node init complete')
        rospy.Subscriber('ev3/active_mode', String, self.active_mode_callback, queue_size=1)
        self.power_init()
        self.touch_init()
        print('READY!')
        rospy.spin()

    def active_mode_callback(self, data):
        print(data)
        try:
            # rospy.logdebug('Active mode: {}'.format(data))
            self.active_mode = data.data
            self.check_thread()
            if data.data == 'stop':
                self.halt()
            elif data.data == 'forward':
                self.forward()
            elif data.data == 'backward':
                self.backward()  
            elif data.data == 'left':
                self.left()
            elif data.data == 'right':
                self.right()  
        except Exception as e:
          rospy.logdebug(e)


    def power_init(self):
        thread = threading.Thread(target=self.power_thread, args=("task",))
        thread.daemon = True
        thread.start()
        return thread        

    def power_thread(self, arg):
        while True:
            try:
                print('{} V'.format(self.power.measured_voltage/1000000))
                print('{} A'.format(self.power.measured_current/1000000))
                sleep(2)
            except Exception as e:
                rospy.logdebug(e)
                break

    def touch_init(self):
        thread = threading.Thread(target=self.touch_thread, args=("task",))
        thread.daemon = True
        thread.start()
        return thread

    def touch_thread(self, arg):
        while True:
            if (self.ts.is_pressed==1):
                self.drive_for_time(-100, 1)

    def check_thread(self):
        while not self.exit:
            sleep(0.5)
        while not self.callback_exit:
            sleep(0.5)


    def forward(self):
        speed = 100
        self.tank_drive.on(SpeedPercent(speed), SpeedPercent(speed))

    def backward(self):
        speed = 100
        self.tank_drive.on(SpeedPercent(-speed), SpeedPercent(-speed))

    def drive_for_time(self, speed, time):
        self.tank_drive.on_for_seconds(SpeedPercent(speed), SpeedPercent(speed), time)

    def left(self):
        speed = 50
        self.tank_drive.on(SpeedPercent(-speed), SpeedPercent(speed))  

    def right(self):
        speed = 50
        self.tank_drive.on(SpeedPercent(speed), SpeedPercent(-speed))           

    def halt(self):
        self.tank_drive.on(SpeedPercent(0), SpeedPercent(0))


if __name__ == '__main__':
    e = EV3DEV()
