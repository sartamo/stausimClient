import logging
import atexit
import time
import os
import configparser

import communication
import motors

def exit_handler():
    logging.info("Exiting program")
    wheellb.setspeed(0)
    wheelrb.setspeed(0)
    wheellf.setspeed(0)
    wheelrf.setspeed(0)
    s.close()

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)

    wheellb = motors.Wheel(config.getint('leftback', 'pin1'), config.getint('leftback', 'pin2'))
    wheelrb = motors.Wheel(config.getint('rightback', 'pin1'), config.getint('rightback', 'pin2'))
    wheellf = motors.Wheel(config.getint('leftfront', 'pin1'), config.getint('leftfront', 'pin2'))
    wheelrf = motors.Wheel(config.getint('rightfront', 'pin1'), config.getint('rightfront', 'pin2'))

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    atexit.register(exit_handler)
    s = communication.Socket(config.get('socket', 'ip'), config.getint('socket', 'port'))
    s.setup()
    while True:
        time.sleep(2)
        s.send(b"Hello from client")
        wheellb.setspeed(0.2)
        wheelrb.setspeed(0.2)
        wheellf.setspeed(0.2)
        wheelrf.setspeed(0.2)