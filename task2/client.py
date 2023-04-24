import socket
import time
import os

def SEND(data,client_socket):                                                   #Function to send data to server
    total_sent = 0                                                              #Total data sent
    while total_sent < len(data):                                               #Loop to send data in chunks
        sent = client_socket.send(data[total_sent:].encode())                   #Sending data
        if sent == 0:                                                           #If no data is sent
            raise RuntimeError("Socket connection broken")                      #Raise error
        total_sent += sent                                                      #Increment total data sent

def chat(id,client_socket):                                                     #Function to chat with other users
        print("Now you can start messaging.")   
        while True:                                                             #Loop to send and receive messages
                print("Type 'exit' to exit from chat room")     
                message = input(id+": ")        
                SEND(message,client_socket)                                     #Send message to the chat room
                time.sleep(0.5)                                                 #Sleep for 0.5 seconds
                if message == "exit":                                           #If message is exit
                        print(client_socket.recv(1024).decode())                #Receive response
                        return                                                  #Return to chat room options
                conversation = client_socket.recv(1024).decode()                #Receive message
                convo  = conversation.split(",")                                #Split message
                os.system('clear')                                              #Clear screen
                for x in convo:                                                 #Loop to print messages
                        print(x)        

def chatRoomOptions(id,client_socket):                                          #Function to show chat room options
        while True:                                                             #Loop to show chat room options
                print("1. Join a chat room")    
                print("2. Create a chat room")
                print("3. Logout")
                choice = input("Enter your choice: ")                           #Input choice
                if choice == "1":       
                        roomID = input("Enter Chat Room ID to join: ")          #Input chat room id
                        msg = "join_"+roomID                                    #Create message
                        SEND(msg,client_socket)                                 #Send join room message
                        response = client_socket.recv(1024).decode()            #Receive response
                        if(response == "1"):    
                                print("Joined Chat Room")
                                print("----Active Users in Chat Room "+roomID+"---")    #Print Active users in chat room
                                print(client_socket.recv(1024).decode())       
                                print("-------------------------------------------")
                                SEND("Received",client_socket)                  #Send acknowledgement
                                chat(id,client_socket)                          #Call chat function
                        else:
                                print(response)    #Print response
                elif choice == "2":
                        roomID = input("Enter Chat Room ID to create: ")        #Input chat room id
                        msg = "create_"+roomID                                  #Create message
                        SEND(msg,client_socket)                                 #Send create room message
                        response = client_socket.recv(1024).decode()
                        print(response)
                elif choice == "3":
                        msg = "logout"  
                        SEND(msg,client_socket)                                 #Send logout message
                        response = client_socket.recv(1024).decode()
                        print(response)
                        break

def client_program():                                                           #Function to connect to server
        host = socket.gethostname()                                             #Get host name
        port = 12344                                                            #Define port
        client_socket = socket.socket()                                         #Create socket  
        client_socket.connect((host, port))                                     #Connect to server
        while True:                                                             #Loop to show login and register options
                choice = input("1. Register\n2. Login\nEnter your choice: ")    #Input choice
                if choice == "1":
                        id = input("Enter your userid to register: ")
                        password = input("Enter your password to registred: ")
                        credentials = "register_"+id+"_"+password               
                        SEND(credentials,client_socket)                         #Send register message
                        response = client_socket.recv(1024).decode()
                        print(response)
                elif choice == "2":
                        id = input("Enter your userid to login: ")
                        password = input("Enter your password to login: ")
                        credentials = "login_"+id+"_"+password
                        SEND(credentials,client_socket)                         #Send login message
                        response = client_socket.recv(1024).decode()
                        print(response)
                        if response == "Login Successful":
                                print("----Active Users-----")
                                print(client_socket.recv(1024).decode())        #Print active users
                                print("---------------------")
                                chatRoomOptions(id,client_socket)
                        else:
                                client_socket.close() 
                        break
                else:
                        print("Wrong Choice")
        client_socket.close() 


if __name__ == '__main__':
    client_program()
