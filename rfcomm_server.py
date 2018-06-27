'''
Created on Apr 16, 2018

@author: broihier
'''
import bluetooth
import Lock
import Switch

class BluetoothServer(object):
    '''
    Bluetooth server class
    '''
    def __init__(self):
        self.switch = Switch.Switch(2)
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)
        uuid = "00000003-0000-1000-8000-00805f9b34fb"
        bluetooth.advertise_service(self.server_socket, "rfcomm",
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE], )
    def run_server(self):
        '''
        Run Server method - this starts the server
        '''
        print("bluetooth RFCOMM server is listening")
        last_seed = 0
        lock = None
        while True:
            client = None
            try:
                client, address = self.server_socket.accept()
                print("Connection accepted")
                while True:
                    data = client.recv(1024)
                    if data:
                        if lock is None:
                            print("Making a lock - this should fail to authenticate")
                            lock = Lock.Lock(data, last_seed)
                        else:
                            print("Checking a new incoming key")
                            lock.check_another_key(data)
                        if lock.is_locked():
                            print("Data is not of the expected pattern")
                            client.send("Authentication Failed")
                        else:
                            print("Data pattern is acceptable")
                            self.switch.press()
                            client.send("Command Successful")

            except KeyboardInterrupt:
                print("Closing socket and exiting")
                if client:
                    client.close()
                break
            except Exception as err:
                print(err)
                print("Closing socket")
                client.close()

        self.server_socket.close()

if __name__ == "__main__":
    SERVER = BluetoothServer()
    SERVER.run_server()
