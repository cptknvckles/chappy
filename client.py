import socket
import threading

# Global client socket
client = None

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'CMD':
                client.send(command.encode('utf-8'))
            elif message == 'USR':
                client.send(username.encode('utf-8'))
            elif message == 'PWD':
                client.send(password.encode('utf-8'))
            elif 'successful' in message:
                print(message)
                if 'Registration' in message:
                    client.close()
                    return
            else:
                print(message)
        except Exception as e:
            if not client._closed:
                print("An error occurred:", e)
            break

def write():
    while True:
        try:
            message = input("")
            if message.strip().upper() == "BYE":
                client.send("BYE".encode('utf-8'))
                client.close()
                break
            client.send(f'{nickname}: {message}'.encode('utf-8'))
        except Exception as e:
            print("An error occurred while sending a message:", e)
            break

def connect_and_authenticate():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 55556))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

command = input('Do you want to [register] or [login]? ').strip().lower()
username = input('Enter your username: ').strip()
password = input('Enter your password: ').strip()

if command == 'register':
    connect_and_authenticate()
    print('Please login after registration.')

if command == 'login':
    connect_and_authenticate()
    nickname = username













# import socket
# import threading

# #client setup
# nickname = input('Choose your username: ')
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# client.connect(('localhost', 55556)) #ensure this matches the server host and port on backend
# #define the receive function
# def receive():
#     while True:
#         try:
#             #receive messages from the server
#             message = client.recv(1024).decode('utf-8')
#             if message == 'NICK':
#                 client.send(nickname.encode('utf-8'))
#             else:
#                 print(message)
#         except:
#             #close connection when error occurs
#             if not client._closed:
#                 print("An error occured!")
#             break
# #now lets define the write function, which will handle sending messages from the user to the server
# def write():
#     while True:
#         message = input("")
#         if message.strip().upper() == "BYE":
#             client.send("BYE".encode('utf-8'))
#             client.close()
#             break
#         client.send(f'{nickname}: {message}'.encode('utf-8'))
# #to allow simultaneous sending and receiving of messages we need to run the receive and write functions in seperate threads
# receive_thread = threading.Thread(target=receive)
# receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()