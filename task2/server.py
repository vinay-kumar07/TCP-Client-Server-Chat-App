import socket
import threading
import time
from datetime import datetime

Users = {}                                                                          # id:password
ActiveUsers = {}                                                                    # id:password
UsersInChatRooms = {}                                                               # roomID:[id1,id2,id3]
Conversations = {}                                                                  # roomID:[conversation]

def SEND(data,client_socket):                                                       # This function is used to send data to client
    total_sent = 0                                                                  # total bytes sent
    while total_sent < len(data):                                                   # loop until all bytes sent
        sent = client_socket.send(data[total_sent:].encode())                       # send data
        if sent == 0:                                                               # if no data sent, raise error
            raise RuntimeError("Socket connection broken")                          # raise error
        total_sent += sent                                                          # add sent bytes to total_sent

def registerUser(msg):                                                              # This function is used to register user
    id = msg.split("_")[1]                                                          # get id from message
    password = msg.split("_")[2]                                                    # get password from message
    if id not in Users:                                                             # if id not in Users
        Users[id] = password                                                        # add id and password to Users

def login(msg):                                                                     # This function is used to login user
    id = msg.split("_")[1]                                                          # get id from message
    password = msg.split("_")[2]                                                    # get password from message
    if id in Users:                                                                 # if id in Users
        if Users[id] == password:                                                   # if password matches
            ActiveUsers[id] = password                                              # add id and password to ActiveUsers
            return 1
        else:                                                                       # if password does not match
            return 0
    else:                                                                           # if id not in Users
        return 0
    
def chat(id,roomID,client_socket):                                                  # This function is used to chat in a chat room
    while True:                                                                     # loop until exit
        message = client_socket.recv(1024).decode()                                 # receive message
        if message == "exit":                                                       # if message is exit
            UsersInChatRooms[roomID].remove(id)                                     # remove id from UsersInChatRooms
            SEND("Leaved Room Successfully",client_socket)                          # send message to client
            return                                                                  # return from function
        message = id+"["+datetime.now().strftime("%I:%M:%S %p")+"]: "+message       # add id and time to message
        Conversations[roomID].append(message)                                       # add message to Conversations
        convo = ','.join(Conversations[roomID])                                     # join all messages in Conversations
        SEND(convo,client_socket)                                                   # send all messages to client
        time.sleep(0.5)                                                             # sleep for 0.5 seconds

def joinRoom(id,roomID,client_socket):                                              # This function is used to join a chat room
    if roomID in UsersInChatRooms:                                                  # if roomID in UsersInChatRooms
        UsersInChatRooms[roomID].append(id)                                         # add id to UsersInChatRooms
        SEND("1",client_socket)                                                     # send 1 to client
        time.sleep(0.2)                                                             # sleep for 0.2 seconds
        actusr = ""                                                                 # active users
        for x in UsersInChatRooms[roomID]:                                          # loop through all users in room
            actusr = actusr + x + ","                                               # add user to actusr
        actusr = actusr[:-1]                                                        # remove last comma
        print(actusr)   
        SEND(actusr,client_socket)                                                  # send actusr to client
        time.sleep(0.2)                                                             # sleep for 0.2 seconds
        print(client_socket.recv(1024).decode())                                    # receive message from client
        chat(id,roomID,client_socket)                                               # call chat function
    else:                                                                           # if roomID not in UsersInChatRooms
        msg = "Chat Room "+roomID+" does not exist"                                 # send message to client
        SEND(msg,client_socket)                                                     # send message to client
    

def createRoom(id,roomID,client_socket):                                            # This function is used to create a chat room
    if roomID not in UsersInChatRooms:                                              # if roomID not in UsersInChatRooms
        UsersInChatRooms[roomID] = []                                               # add roomID to UsersInChatRooms
        Conversations[roomID] = []                                                  # add roomID to Conversations
        msg = "Chat Room "+roomID+" Created Successfully"                           # send message to client
        SEND(msg,client_socket)                                                     # send message to client
    else:                                                                           # if roomID in UsersInChatRooms
        msg = "Chat Room "+roomID+" already exist"                                  # send message to client
        SEND(msg,client_socket)                                                     # send message to client

def roomActions(client_socket,id):                                                  # This function is used to perform actions in chat room
    while True:                                                                     # loop until logout
        msg = client_socket.recv(1024).decode()                                     # receive message from client
        print(msg)                                                                  # print message
        if msg == "logout":                                                         # if message is logout
            SEND("Logged Out Successfully",client_socket)                           # send message to client
            return                                                                  # return from function
        verb = msg.split("_")[0]                                                    # get verb from message
        roomID = msg.split("_")[1]                                                  # get roomID from message
        if verb == "join":                                                          # if verb is join
            joinRoom(id,roomID,client_socket)                                       # call joinRoom function
        elif verb == "create":                                                      # if verb is create
            createRoom(id,roomID,client_socket)                                     # call createRoom function

def handle_connection(client_socket,client_address):                                # This function is used to handle connection
    id = ""                                                                         # id of user
    while True:                                                                     # loop until login
        msg = client_socket.recv(1024).decode()                                     # receive message from client
        if msg.split("_")[0] == "register":                                         # if message is register
            registerUser(msg)                                                       # call registerUser function
            SEND("User Registered Successfully, Now you can Login",client_socket)   # send message to client
        elif msg.split("_")[0] == "login":                                          # if message is login
            if login(msg):                                                          # call login function
                id = msg.split("_")[1]                                              # get id from message
                SEND("Login Successful",client_socket)                              # send message to client
                time.sleep(0.02)                                                    # sleep for 0.02 seconds
                actusr = ""                                                         # active users
                for x in ActiveUsers:                                               # loop through all active users
                    actusr = actusr + x + ","                                       # add user to actusr
                actusr = actusr[:-1]                                                # remove last comma
                SEND(actusr,client_socket)                                          # send actusr to client
                time.sleep(0.1)                                                     # sleep for 0.1 seconds
                roomActions(client_socket,id)                                       # call roomActions function
                ActiveUsers.pop(id)                                                 # remove id from ActiveUsers
            else :                                                                  # if login function returns 0
                SEND("Wrong Credentials",client_socket)                             # send message to client
                client_socket.close()                                               # close connection
            break                                                                   # break from loop

    client_socket.close()                                                           # close connection

def server_program():                                                               # This function is used to start server
    host = socket.gethostname()                                                     # get host name
    port = 12344                                                                    # initiate port
    server_socket = socket.socket()                                                 # initiate socket
    server_socket.bind((host, port))                                                # bind host and port
    server_socket.listen(2)                                                         # listen for connections
    while True:                                                                     # loop forever
        client_socket, client_address = server_socket.accept()                      # accept connection
        print("Connection from: ", str(client_address))                             # print client address
        thread = threading.Thread(target=handle_connection, args=(client_socket,client_address))    # create thread
        thread.daemon = True                                                        # set daemon to true
        thread.start()                                                              # start thread


if __name__ == '__main__':
    server_program()
