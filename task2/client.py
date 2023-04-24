import socket
import time

def SEND(data,client_socket):
    total_sent = 0
    while total_sent < len(data):
        sent = client_socket.send(data[total_sent:].encode())
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent

def chat(id,client_socket):
        #send message to chat room
        print("Now you can start messaging.Type 'exit' to exit from chat room")
        while True:
                message = input(id+": ")
                SEND(message,client_socket)
                time.sleep(0.5)
                # client_socket.send(message.encode())
                if message == "exit":
                        print(client_socket.recv(1024).decode())
                        return
                print(client_socket.recv(1024).decode())

def chatRoomOptions(id,client_socket):
        print("1. Join a chat room")
        print("2. Create a chat room")
        print("3. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
                roomID = input("Enter Chat Room ID to join: ")
                msg = "join_"+roomID
                SEND(msg,client_socket)
                # client_socket.send(msg.encode())
                response = client_socket.recv(1024).decode()
                print(response)
                if(response == "1"):
                        print("Joined Chat Room")
                        print("----Active Users in Chat Room "+roomID+"------")
                        print(client_socket.recv(1024).decode())
                        print("-------------------------------------------------")
                        SEND("Received",client_socket)
                        # client_socket.send("Received".encode())
                        chat(id,client_socket)

        elif choice == "2":
                roomID = input("Enter Chat Room ID to create: ")
                msg = "create_"+roomID
                SEND(msg,client_socket)
                # client_socket.send(msg.encode())
                response = client_socket.recv(1024).decode()
                print(response)

        elif choice == "3":
                msg = "logout"
                SEND(msg,client_socket)
                # client_socket.send(msg.encode())
                response = client_socket.recv(1024).decode()
                print(response)

def client_program():

        host = socket.gethostname() 
        port = 12344 

        client_socket = socket.socket()  
        client_socket.connect((host, port)) 
        
        while True:
                choice = input("1. Register\n2. Login\nEnter your choice: ")
                if choice == "1":
                        # send userid and password to register to server
                        id = input("Enter your userid to register: ")
                        password = input("Enter your password to registred: ")
                        credentials = "register_"+id+"_"+password
                        SEND(credentials,client_socket)
                        # client_socket.send(credentials.encode())
                        response = client_socket.recv(1024).decode()
                        print(response)

                elif choice == "2":
                        #send userid and password to login to server
                        id = input("Enter your userid to login: ")
                        password = input("Enter your password to login: ")
                        credentials = "login_"+id+"_"+password
                        SEND(credentials,client_socket)
                        # client_socket.send(credentials.encode())
                        response = client_socket.recv(1024).decode()
                        print(response)
                        if response == "Login Successful":
                                chatRoomOptions(id,client_socket)
                        else:
                                client_socket.close() 
                        break
                else:
                        print("Wrong Choice")
        client_socket.close() 


if __name__ == '__main__':
    client_program()
