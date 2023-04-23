import socket

def server_program():
    host = socket.gethostname()
    port = 12344 

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: ", str(address))

    msg = conn.recv(1024).decode()
    print(msg)
    conn.send("hello from server".encode())

    conn.close() 


if __name__ == '__main__':
    server_program()
