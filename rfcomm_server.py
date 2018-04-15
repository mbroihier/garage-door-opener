import socket 
import bluetooth
import Lock
address = 'B8:27:EB:69:B1:42'
port = 5
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))
server_socket.listen(1)
port = server_socket.getsockname()[1]
uuid = "00000003-0000-1000-8000-00805f9b34fb"
bluetooth.advertise_service( server_socket, "rfcomm",
                             service_id = uuid,
                             service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                             profiles = [ bluetooth.SERIAL_PORT_PROFILE ],)
while True:
    try:
        client, address = server_socket.accept()
        print("Connection accepted")
        while True:
            data = client.recv(1024)
            if data:
                print(data)
                print("Making lock")
                lock = Lock.Lock(data)
                print("Checking lock")
                if lock.isLocked():
                    print("Data is not of the expected pattern")
                    client.send("Authentication Error")
                else:
                    print("Data pattern is acceptable")
                    client.send("Command accepted")
                #client.send(data)
    except KeyboardInterrupt:
        print("Closing socket and exiting")
        client.close()
        break 
    except Exception as Err :
        print(Err)
        print("Closing socket")
        client.close()

server_socket.close()
