import socket

def client_program():

        host = socket.gethostname() 
        port = 12344 

        client_socket = socket.socket()  
        client_socket.connect((host, port)) 

        # send userid and password to register to server
        id = input("Enter your userid to register: ")
        password = input("Enter your password to registred: ")
        credentials = id+"_"+password
        client_socket.send(credentials.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        #send userid and password to login to server
        id = input("Enter your userid to login: ")
        password = input("Enter your password to login: ")
        credentials = id+"_"+password
        client_socket.send(credentials.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.close() 


if __name__ == '__main__':
    client_program()
