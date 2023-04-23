import socket

def client_program():

        host = socket.gethostname() 
        port = 12344 

        client_socket = socket.socket()  
        client_socket.connect((host, port)) 

        try:
                fp = open("inputFilesPath.txt", "r")
        except:
                print("Error: inputFilesPath.txt not found")
                exit(1)
        path = fp.read()
        fp.close()

        #send file name to server
        filename = input("Enter file name: ")
        client_socket.sendall(filename.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        #read file data and send to server
        try:  
                fp = open(path, "rb")
        except:
                print("Error: File not found")
                exit(1)
        client_socket.sendall(fp.read())
        fp.close()

        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.close() 


if __name__ == '__main__':
    client_program()
