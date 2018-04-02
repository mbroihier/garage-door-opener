'''
Created on Apr 2, 2018

@author: broihier
'''
import socket

class bluetooth_client(object):
    '''
    Client to test bluetooth server for garage door opener
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.address = 'B8:27:EB:69:B1:42'
        self.port = 5
        
    def client(self):
        print('Entering client')
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.connect((self.address, self.port))
        s.send(bytes('test', 'UTF-8'))
        s.send(bytes('it works', 'UTF-8'))
        s.close()
        print('done')
        
if __name__ == '__main__':
    client = bluetooth_client()
    client.client()