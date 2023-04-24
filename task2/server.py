import socket
import threading
import time

Users = {}
ActiveUsers = {}
UsersInChatRooms = {}
AddressInChatRooms = {}

# function to show active users
def showActiveUsers(ActiveUsers):
    print("----Active Users-----")
    for key in ActiveUsers:
        print(key)
    print("---------------------")

# function to register user
def registerUser(msg):
    id = msg.split("_")[1]
    password = msg.split("_")[2]
    if id not in Users:
        Users[id] = password

# function to login user
def login(msg):
    id = msg.split("_")[1]
    password = msg.split("_")[2]
    if id in Users:
        if Users[id] == password:
            ActiveUsers[id] = password
            showActiveUsers(ActiveUsers)
            return 1
        else:
            return 0
    else:
        return 0
    
def SEND(data,client_socket):
    total_sent = 0
    while total_sent < len(data):
        sent = client_socket.send(data[total_sent:].encode())
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

# function to handle chat room
def chat(id,roomID,client_socket):
    #receive message from client and send only to the clients in the chat room
    while True:
        message = client_socket.recv(1024).decode()
        if message == "exit":
            UsersInChatRooms[roomID].remove(id)
            AddressInChatRooms[roomID].remove(client_socket)
            SEND("Leaved Room Successfully",client_socket)
            # client_socket.send("Leaved Room Successfully".encode())
            return
        message = id+": "+message
        for activeClientsInChatRoom in AddressInChatRooms[roomID]:
            if activeClientsInChatRoom!=client_socket:
                SEND(message,activeClientsInChatRoom)
                time.sleep(0.1)
                # activeClientsInChatRoom.send(message.encode())
        SEND("Sent",client_socket)
        time.sleep(0.1)

# function to join chat room
def joinRoom(id,roomID,client_socket):
    if roomID in UsersInChatRooms:
        UsersInChatRooms[roomID].append(id)
        AddressInChatRooms[roomID].append(client_socket)
        # client_socket.send("1".encode())
        SEND("1",client_socket)
        time.sleep(0.2)
        #send active users in chat room
        actusr = ""
        for x in UsersInChatRooms[roomID]:
            actusr = actusr + x + ","
        actusr = actusr[:-1]
        print(actusr)
        # client_socket.send(actusr.encode())
        SEND(actusr,client_socket)
        time.sleep(0.2)
        print(client_socket.recv(1024).decode())

        chat(id,roomID,client_socket)
  
    else:
        msg = "Chat Room "+roomID+" does not exist"
        SEND(msg,client_socket)
        # client_socket.send(msg.encode())
        return
    

# function to create chat room
def createRoom(id,roomID,client_socket):
    if roomID not in UsersInChatRooms:
        UsersInChatRooms[roomID] = []
        AddressInChatRooms[roomID] = []
        msg = "Chat Room "+roomID+" Created Successfully"
        # client_socket.send(msg.encode())
        SEND(msg,client_socket)

    else:
        msg = "Chat Room "+roomID+" already exist"
        # client_socket.send(msg.encode())
        SEND(msg,client_socket)

# function to handle room actions
def roomActions(client_socket,id):
    # receive room id to join or create
    msg = client_socket.recv(1024).decode()
    print(msg)
    if msg == "logout":
        SEND("Logged Out Successfully",client_socket)
        # client_socket.send("Logged Out Successfully".encode())
        return
    verb = msg.split("_")[0]
    roomID = msg.split("_")[1]
    if verb == "join":
        joinRoom(id,roomID,client_socket)
    elif verb == "create":
        createRoom(id,roomID,client_socket)

# function to handle connection
def handle_connection(client_socket,client_address):
    id = ""
    while True:
        # receive userid and password from client to register/Login
        msg = client_socket.recv(1024).decode()
        if msg.split("_")[0] == "register":
            registerUser(msg)
            SEND("User Registered Successfully, Now you can Login",client_socket)
            # client_socket.send("User Registered Successfully, Now you can Login".encode())
        elif msg.split("_")[0] == "login":
            if login(msg):
                id = msg.split("_")[1]
                SEND("Login Successful",client_socket)
                # client_socket.send("Login Successful".encode())
                roomActions(client_socket,id)
                ActiveUsers.pop(id)
            else : 
                SEND("Wrong Credentials",client_socket)
                # client_socket.send("Wrong Credentials".encode())
                client_socket.close()
            break

    client_socket.close()

# function to start server
def server_program():
    host = socket.gethostname()
    port = 12344 

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from: ", str(client_address))

        # handle_connection(client_socket,client_address)
        thread = threading.Thread(target=handle_connection, args=(client_socket,client_address))
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    server_program()
