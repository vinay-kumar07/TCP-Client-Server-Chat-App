import socket

Users = {}
ActiveUsers = {}
UsersInChatRooms = {}

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

    id = ""
    password = ""
    
    # receive userid and password from client to register
    msg = conn.recv(1024).decode()
    registerUser(msg)
    conn.send("User Registered Successfully, Now you can Login".encode())

    # receive userid and password from client to login
    msg = conn.recv(1024).decode()
    if login(msg):
        id = msg.split("_")[0]
        password = msg.split("_")[1]
        conn.send("Login Successful".encode())
    else : 
        conn.send("Wrong Credentials".encode())

    # receive room id to join or create
    msg = conn.recv(1024).decode()
    verb = msg.split("_")[0]
    roomID = msg.split("_")[1]
    if verb == "join":
        if roomID in UsersInChatRooms:
            UsersInChatRooms[roomID].append(id)
            msg = "Joined Chat Room "+roomID+" Successfully"
            conn.send(msg.encode())

        else:
            msg = "Chat Room "+roomID+" does not exist"
            conn.send(msg.encode())
    
    elif verb == "create":
        if roomID not in UsersInChatRooms:
            UsersInChatRooms[roomID] = []
            msg = "Chat Room "+roomID+" Created Successfully"
            conn.send(msg.encode())
        else:
            msg = "Chat Room "+roomID+" already exist"
            conn.send(msg.encode())

    conn.close() 


if __name__ == '__main__':
    server_program()
