from gpiozero import Motor
from time import sleep
import logging

class Wheel:
    def __init__(self, position, ports): 
        self.position = position # Position is a tuple (x, y): can be each 0 or 1, (0, 0) is back left, (1, 1) is front right
        self.motor = Motor(ports[0], ports[1])
        self.speed = 0 # Between -1 and 1, where -1 is full reverse, 0 is stop, and 1 is full forward

    def setspeed(self):
        if self.speed > 0:
            self.motor.forward(self.speed)
        elif self.speed < 0:
            self.motor.backward(-self.speed)
        else:
            self.motor.stop()
        logging.info(f"Motor speed set to {self.speed} for motor at {self.position}")

wheel = Wheel((0, 0), (2, 3))

wheel.speed = 0
wheel.setspeed()
while True:
    sleep(0.5)
    if wheel.speed <= 0.95:
        wheel.speed += 0.05
        wheel.setspeed()
        print(f"Motor speed set to {wheel.speed}")
