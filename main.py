import logging
import atexit
import os
import configparser
import pickle

import communication
import motors

def exit_handler():
    logging.info("Exiting program")
    wheellb.motor.close()
    wheelrb.motor.close()
    wheellf.motor.close()
    wheelrf.motor.close()
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

    wheellb.setspeed(0)
    wheelrb.setspeed(0)
    wheellf.setspeed(0)
    wheelrf.setspeed(0)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    atexit.register(exit_handler)
    s = communication.Socket(config.get('socket', 'ip'), config.getint('socket', 'port'))
    s.setup()
    while True:
        if s.status == 0:
            wheellb.setspeed(0)
            wheelrb.setspeed(0)
            wheellf.setspeed(0)
            wheelrf.setspeed(0)
        else:
            data = s.receive()
            if data:
                (angle, speed) = pickle.loads(data)
                logging.info(f"Received data: angle = {angle}, speed = {speed}")

                '''lf, rf, lb, rb = motors.mecanum(angle, speed)
                wheellb.setspeed(lb)
                wheelrb.setspeed(rb)
                wheellf.setspeed(lf)
                wheelrf.setspeed(rf)'''

                speeds = [config.getint('speeds', '1')/100, config.getint('speeds', '2')/100, config.getint('speeds', '3')/100]

                wheellb.setspeed(speeds[speed] * config.getint('leftback', 'speed') / 100)
                wheelrb.setspeed(speeds[speed] * config.getint('rightback', 'speed') / 100)
                wheellf.setspeed(speeds[speed] * config.getint('leftfront', 'speed') / 100)
                wheelrf.setspeed(speeds[speed] * config.getint('rightfront', 'speed') / 100)

            