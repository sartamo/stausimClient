from gpiozero import Motor
from time import sleep
import logging
import configparser
import os
import math

def mecanum(angle, magnitude):
    assert magnitude <= 1 and magnitude >= 0 # speeds between 0 and 1 allowed

    rf = math.sin(angle - math.pi / 4) * magnitude
    lb = rf

    lf = math.sin(angle + math.pi / 4) * magnitude
    rb = lf

    return lf, rf, lb, rb

class Wheel:
    def __init__(self, port1, port2): 
        self.motor = Motor(port1, port2)
        self.port1 = port1
        self.port2 = port2
        self.speed = 0 # Between -1 and 1: -1 full reverse, 0 stop, and 1 full forward

    def setspeed(self, speed):
        self.speed = speed
        if self.speed > 0:
            self.motor.forward(self.speed)
        elif self.speed < 0:
            self.motor.backward(-self.speed)
        else:
            self.motor.stop()
        logging.info(f"Motor speed set to {self.speed} at ports {self.port1}, {self.port2}")

script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

wheellb = Wheel(config.getint('leftback', 'pin1'), config.getint('leftback', 'pin2'))
wheelrb = Wheel(config.getint('rightback', 'pin1'), config.getint('rightback', 'pin2'))
wheellf = Wheel(config.getint('leftfront', 'pin1'), config.getint('leftfront', 'pin2'))
wheelrf = Wheel(config.getint('rightfront', 'pin1'), config.getint('rightfront', 'pin2'))

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    angle = 0
    while True:
        sleep(0.1)
        angle += 0.1
        lf, rf, lb, rb = mecanum(angle, 0.1)
        wheellb.setspeed(lb)
        wheelrb.setspeed(rb)
        wheellf.setspeed(lf)
        wheelrf.setspeed(rf)

