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
        print(f"Motor speed set to {self.speed} for motor at {self.position}")

wheel1 = Wheel((0, 0), (2, 3))
wheel2 = Wheel((0, 1), (4, 14))
wheel3 = Wheel((1, 0), (22, 23))
wheel4 = Wheel((1, 1), (27, 17))

wheel1.speed = 0
wheel1.setspeed()
wheel2.speed = 0
wheel2.setspeed()
wheel3.speed = 0
wheel3.setspeed()
wheel4.speed = 0
wheel4.setspeed()
while True:
    sleep(0.5)
    if wheel1.speed <= 0.95:
        print(f"speed increased to {wheel1.speed}")
        wheel1.speed += 0.05
        wheel1.setspeed()
        wheel2.speed += 0.05
        wheel2.setspeed()
        wheel3.speed += 0.05
        wheel3.setspeed()
        wheel4.speed += 0.05
        wheel4.setspeed()
