import socket

def client_program():

        host = socket.gethostname() 
        port = 12344 

        client_socket = socket.socket()  
        client_socket.connect((host, port)) 

        msg = "Hello Server"
        client_socket.send(msg.encode()) 
        data = client_socket.recv(1024).decode() 
        print(data)
  
        client_socket.close() 


if __name__ == '__main__':
    client_program()
