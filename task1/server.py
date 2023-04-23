import socket

def server_program():
    host = socket.gethostname()
    port = 12344 

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: ", str(address))
    
    #read file name from client
    filename = conn.recv(1024).decode()
    conn.send("File Name Received".encode())  

    #read file data from client and store in database
    storePath = "ServerDatabase/" + filename
    fp = open(storePath, "wb")
    while True:
        #receive data from client in 1024 byte chunks and dont block if no data is received for 2 seconds
        conn.settimeout(2)
        try:
            data_received = conn.recv(1024)
        except socket.timeout:
            break
        if not data_received:
            break
        fp.write(data_received)
    fp.close()

    conn.send("Data Received and Stored in Server Database.".encode())  
    conn.close() 


if __name__ == '__main__':
    server_program()
