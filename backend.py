import socket
import threading
#server setup
host = 'localhost' #localhost
port = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a new socket using IPv4(AF_INET) and TCP(SOCK_STREAM)
server.bind((host, port)) #binds the socket to the specified host and port
server.listen() #puts the socket into listening mode, ready to accept connections

#accepting clients
clients = []
nicknames = []

#broadcasting messages
#we need to define the 'broadcast' function that sends a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)
    #this function iterates over all clients and sends the given message to each one
#defining the 'handle_client' function to manage communication with a connected client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8').strip() == "BYE":
                index = clients.index(client)
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                break
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break
#define a function that will accept new clients and start a new thread for each client to handle comms
def receive():
    while True:
            client, address = server.accept() #accepts a new connection and returns the client socket and address
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('utf-8'))#asks the client for their username(nickname)
            nickname = client.recv(1024).decode('utf-8')#receives the nicname from client
            nicknames.append(nickname)#adds nickname to the array
            clients.append(client)#adds client to the array

            print(f"username is {nickname}")
            broadcast(f"{nickname} joined the chat!".encode('utf-8'))
            client.send("\nconnected to the server".encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client,))#creates a new thread to handle comms with this client
            thread.start()
        


#starting the server
print('Server is listening...')
receive()