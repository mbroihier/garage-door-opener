'''
Created on Jun 16, 2018

@author: broihier
'''
import sys
import time
import bluetooth

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
    def __init__(self):
        uuid = "00000003-0000-1000-8000-00805f9b34fb"
        address = "B8:27:EB:69:B1:42"
        service_matches = bluetooth.find_service(
            uuid=uuid,
            address=address)
        if not service_matches:
            print("no service found")
            sys.exit(0)
        for match in service_matches:
            self.host = match["host"]
            print(self.host)
            self.port = match["port"]
            print(self.port)
            name = match["name"]
            print(name)

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

    def gdo_driver(self, control_path):
        '''
        GDO Controller driver
        '''
        file_object = open(control_path, "r")
        line = file_object.readline()
        if line != "":
            test_category_name = line.strip()
        else:
            print("file open error: " + control_path)
            exit(-1)
        results = open(test_category_name + ".testDbResults", "w")
        expected_results = open(test_category_name + ".testDbExpectedResults", "r")
        line = file_object.readline()
        while line != "":
            string_bytes = file_object.readline().rstrip().split(" ")
            message_bytes = bytearray()
            for string_byte in string_bytes:
                message_bytes.append(bytes.fromhex(string_byte)[0])
            expected_reply = expected_results.readline()
            expected_reply = expected_results.readline().rstrip()
            expected_reply_bytes = bytes(expected_reply, "utf-8")
            reply = self.run_client(message_bytes)
            if check_bytes(reply, expected_reply_bytes):
                print("Test passed")
                results.write(line)
                results.write("PASSED\n")
            else:
                print("Test failed")
                print("Expected: " + expected_reply)
                print("Received: " + reply.decode("utf-8"))
                results.write(line)
                results.write("FAILED\n")
            line = file_object.readline()

        results.close()
        expected_results.close()

if __name__ == "__main__":
    CLIENT = BluetoothClient()
    CLIENT.gdo_driver(sys.argv[1])
