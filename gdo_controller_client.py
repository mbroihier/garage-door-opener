'''
Created on June 1, 2025

@author: broihier
'''
import sys
import time
import bluetooth
import Lock

def check_bytes(ba1, ba2):
    '''
    Check byte arrays for equality
    '''
    if len(ba1) != len(ba2):
        return False
    index = 0
    for ba1_byte in ba1:
        if ba1_byte != ba2[index]:
            return False
        else:
            index = index + 1
    return True

class BluetoothClient(object):
    '''
    Bluetooth client class
    '''
    def __init__(self, address):

        service_matches = bluetooth.find_service(
            address=address)

        if not service_matches:
            print("no service found")
            sys.exit(0)
        self.host = None
        for match in service_matches:
            if match["name"] == "rfcomm":
                self.host = match["host"]
                self.port = match["port"]
        if self.host is None:
            print("no service found")
            sys.exit(0)

    def run_client(self, message):
        '''
        Run Client method - send packet and receive reply
        '''
        server_socket = None
        while True:
            try:
                server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                server_socket.connect((self.host, self.port))
                break
            except bluetooth.btcommon.BluetoothError:
                server_socket.close()
                time.sleep(2)

        print("sending packet to GDO controller")
        try:
            server_socket.send(bytes(message))
            reply = server_socket.recv(1024)
            server_socket.close()
        except Exception as err:
            print("Error talking to server: " + err)
        return reply

    def gdo_client(self):
        '''
        GDO Controller driver
        '''
        seed = int(time.time())
        seed_bytes = bytearray()
        for _ in range(4):
            seed_bytes.append((seed >> (3 - _)*8) & 0xff)
        lock = Lock.Lock(seed_bytes, 1)
        reply = self.run_client(lock.get_real_key())
        print(reply)


if __name__ == "__main__":
    CLIENT = BluetoothClient(sys.argv[1])
    CLIENT.gdo_client()
