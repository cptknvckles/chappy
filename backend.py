import socket
import threading
from db import create_user_table, add_user, authenticate

# Server setup
host = 'localhost'
port = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8').strip().upper() == "BYE":
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

def receive():
    create_user_table()
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('CMD'.encode('utf-8'))
        command = client.recv(1024).decode('utf-8').strip()

        if command == 'register':
            client.send('USR'.encode('utf-8'))
            username = client.recv(1024).decode('utf-8').strip()
            client.send('PWD'.encode('utf-8'))
            password = client.recv(1024).decode('utf-8').strip()

            if add_user(username, password):
                client.send('Registration successful. Please login.'.encode('utf-8'))
            else:
                client.send('Username already exists'.encode('utf-8'))
            client.close()

        elif command == 'login':
            client.send('USR'.encode('utf-8'))
            username = client.recv(1024).decode('utf-8').strip()
            client.send('PWD'.encode('utf-8'))
            password = client.recv(1024).decode('utf-8').strip()

            if authenticate(username, password):
                client.send('Login successful'.encode('utf-8'))
                nicknames.append(username)
                clients.append(client)

                print(f"Username is {username}")
                broadcast(f"{username} joined the chat!".encode('utf-8'))
                client.send("Connected to the server".encode('utf-8'))

                thread = threading.Thread(target=handle_client, args=(client,))
                thread.start()
            else:
                client.send('Invalid username or password'.encode('utf-8'))
                client.close()

print('Server is listening...')
receive()

