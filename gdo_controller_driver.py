'''
Created on Jun 16, 2018

@author: broihier
'''
import sys
import bluetooth
import Lock

def check_bytes(b1, b2):
    '''
    Check byte arrays for equality
    '''
    if len(b1) != len(b2):
        return False
    index = 0
    for b1_byte in b1:
        if b1_byte != b2[index]:
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
            host = match["host"]
            print(host)
            port = match["port"]
            print(port)
            name = match["name"]
            print(name)
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.connect((host, port))
        self.test_data = bytearray()

    def run_client(self, message):
        '''
        Run Client method - send packet and receive reply
        '''
        print("sending packet to GDO controller")
        self.server_socket.send(bytes(message))
        reply = self.server_socket.recv(1024)
        return reply

    def gdo_driver(self, control_path):
        fileObject = open(control_path, "r")
        line = fileObject.readline()
        if line != "":
            test_category_name = line.strip()
        else:
            print("file open error: " + control_path)
            self.close_client()
            exit(-1)
        results = open(test_category_name + ".testDbResults", "w")
        expected_results = open(test_category_name + ".testDbExpectedResults", "r")
        line = fileObject.readline()
        passed_string = bytes("Command Successful", "utf-8")
        while line != "":
            string_bytes = fileObject.readline().rstrip().split(" ")
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
            line = fileObject.readline()

        results.close()
        expected_results.close()
        self.server_socket.close()

    def close_client(self):
        self.server_socket.close()

if __name__ == "__main__":
    CLIENT = BluetoothClient()
    CLIENT.gdo_driver(sys.argv[1])
