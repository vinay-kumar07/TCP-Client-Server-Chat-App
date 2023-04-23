import socket
import random
def server_program():
    host = socket.gethostname()
    port = 12344 

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: ", str(address))
    
    # while True:
    data_received = conn.recv(1024).decode()
    if not data_received:
        # break
        print("No data received")
    
    print(data_received)

    data_sent = "Hello Client" 
    conn.send(data_sent.encode())  

    conn.close() 


if __name__ == '__main__':
    server_program()
