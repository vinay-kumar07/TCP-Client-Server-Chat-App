import socket

def client_program():

        host = socket.gethostname() 
        port = 12344 

        client_socket = socket.socket()  
        client_socket.connect((host, port)) 

        # send userid and password to register to server
        id = input("Enter your userid to register: ")
        password = input("Enter your password to registred: ")
        credentials = id+"_"+password
        client_socket.send(credentials.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        #send userid and password to login to server
        id = input("Enter your userid to login: ")
        password = input("Enter your password to login: ")
        credentials = id+"_"+password
        client_socket.send(credentials.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        if(response == "Login Successful"):
                print("1. Join a chat room")
                print("2. Create a chat room")
                print("3. Logout")
                choice = input("Enter your choice: ")
                if choice == "1":
                        roomID = input("Enter Chat Room ID to join: ")
                        msg = "join_"+roomID
                        client_socket.send(msg.encode())
                        response = client_socket.recv(1024).decode()
                        print(response)
                       
                        if(response == "Joined Chat Room "+roomID+" Successfully"):
                                roomActiveUsers = client_socket.recv(1024).decode()
                                print("----Active Users in Chat Room "+roomID+"------")
                                print(roomActiveUsers)
                                print("-------------------------------------------------")


                elif choice == "2":
                        roomID = input("Enter Chat Room ID to create: ")
                        msg = "create_"+roomID
                        client_socket.send(msg.encode())
                        response = client_socket.recv(1024).decode()
                        print(response)
                elif choice == "3":
                        print("Logout Successful")

        client_socket.close() 


if __name__ == '__main__':
    client_program()
