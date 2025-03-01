import socket
import threading
import logging
import time

class Socket:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.sock = False
        self.sendBuffer = []
        self.receiveBuffer = []
        self.status = 0 # 0: Not connected, 1: Connected
        logging.info(f"Created Socket client object with {self.host} on port {self.port}")
        
    def _setup(self):
        assert self.status == 0 # Raise AssertionError if socket has already been set up
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            logging.info(f"Trying to connect to {self.host} on port {self.port}")
            self.sock.connect((self.host, self.port))
            self.status = 1
            logging.info(f"Connected to {self.host} on port {self.port}")
            s = threading.Thread(target=self._send)
            s.start()
            r = threading.Thread(target=self._receive)
            r.start()
        except ConnectionRefusedError:
            logging.info(f"Failed to connect to {self.host} on port {self.port}. Retrying in 5 seconds ...")
            time.sleep(5)
            self.close() # Close current socket and retry if connection failed
            self.setup()

    def _receive(self):
        while True:
            if self.status != 1: # Something else has closed the connection and will handle it
                break
            data = self.sock.recv(1024)
            if not data:
                logging.info(f"Received empty data from {self.host} on port {self.port}")
                self.close() # If connection is lost, close and retry
                self.setup()
                break
            self.receiveBuffer.append(data)
            logging.info(f"Received {data} from {self.host} on port {self.port}")

    def _send(self):
        while True:
            if self.status != 1: # Something else has closed the connection and will handle it
                break
            if self.sendBuffer:
                try:
                    self.sock.sendall(self.sendBuffer[0])
                    logging.info(f"Sent {self.sendBuffer[0]} to {self.host} on port {self.port}")
                    self.sendBuffer.pop(0)
                except BrokenPipeError:
                    logging.info(f"Couldn't send data to {self.host} on port {self.port}")
                    self.close() # If connection is lost, close and retry
                    self.setup()
                    break
            time.sleep(0.05)

    def receive(self):
        if self.receiveBuffer:
            data = self.receiveBuffer
            self.receiveBuffer.pop(0)
            return data
        else:
            return False
    
    def send(self, data):
        self.sendBuffer.append(data)

    def setup(self):
        x = threading.Thread(target=self._setup)
        x.start()
    
    def close(self):
        self.status = 0
        if self.sock:
            self.sock.close()
            logging.info(f"Closed sock for host {self.host} on port {self.port}")