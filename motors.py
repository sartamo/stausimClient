from gpiozero import Motor
from time import sleep
import logging
import configparser

class Wheel:
    def __init__(self, port1, port2): 
        self.motor = Motor(port1, port2)
        self.port1 = port1
        self.port2 = port2
        self.speed = 0 # Between -1 and 1: -1 full reverse, 0 stop, and 1 full forward

    def setspeed(self):
        if self.speed > 0:
            self.motor.forward(self.speed)
        elif self.speed < 0:
            self.motor.backward(-self.speed)
        else:
            self.motor.stop()
        print(f"Motor speed set to {self.speed} at ports {self.port1}, {self.port2}")

config = configparser.ConfigParser()
config.read('config.ini')

wheellb = Wheel(config.getint('leftback', 'pin1'), config.getint('leftback', 'pin2'))
wheelrb = Wheel(config.getint('rightback', 'pin1'), config.getint('rightback', 'pin2'))
wheellf = Wheel(config.getint('leftfront', 'pin1'), config.getint('leftfront', 'pin2'))
wheelrf = Wheel(config.getint('rightfront', 'pin1'), config.getint('rightfront', 'pin2'))

if __name__ == '__main__':
    wheellf.speed = 1
    wheellf.setspeed()
    while True:
        pass
