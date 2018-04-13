import socket 
address = 'B8:27:EB:69:B1:42'
port = 5
server_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server_socket.bind((address, port))
server_socket.listen(1)
try:
    client, address = server_socket.accept()
    print("Connection accepted")
    while True:
        data = client.recv(1024)
        if data:
            print(data)
            client.send(data)
except:
    print("Closing socket")
    client.close()
    server_socket.close()
