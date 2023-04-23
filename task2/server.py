import socket

Users = {}
ActiveUsers = {}

def showActiveUsers(ActiveUsers):
    print("----Active Users-----")
    for key in ActiveUsers:
        print(key)
    print("---------------------")

def registerUser(msg):
    id = msg.split("_")[0]
    password = msg.split("_")[1]
    Users[id] = password

def login(msg):
    id = msg.split("_")[0]
    password = msg.split("_")[1]
    if id in Users:
        if Users[id] == password:
            showActiveUsers(ActiveUsers)
            return 1
        else:
            return 0
    else:
        return 0

def server_program():
    host = socket.gethostname()
    port = 12344 

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()

    print("Connection from: ", str(address))

    # receive userid and password from client to register
    msg = conn.recv(1024).decode()
    registerUser(msg)
    conn.send("User Registered Successfully, Now you can Login".encode())

    # receive userid and password from client to login
    msg = conn.recv(1024).decode()
    if login(msg):
        conn.send("Login Successful".encode())
    else : 
        conn.send("Wrong Credentials".encode())

    conn.close() 


if __name__ == '__main__':
    server_program()
