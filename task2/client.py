import socket

def client_program():

        host = socket.gethostname() 
        port = 12344 

        client_socket = socket.socket()  
        client_socket.connect((host, port)) 

        client_socket.send("hello from client".encode())
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.close() 


if __name__ == '__main__':
    client_program()
