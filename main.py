import logging
import communication
import atexit
import time

def exit_handler():
    logging.info("Exiting program")
    s.close()

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    atexit.register(exit_handler)
    s = communication.Socket("192.168.2.193", 50000)
    s.setup()
    while True:
        time.sleep(2)
        s.send(b"Hello from client")