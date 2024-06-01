import socket
import threading


#client setup
password = input('enter sever password: ')
nickname = input('Choose your username: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(('localhost', 55556)) #ensure this matches the server host and port on backend
#define the receive function
def receive():
    while True:
        try:
            #receive messages from the server
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
            elif message == 'PASS':
                client.send(password.encode('utf-8'))
            elif message == 'wrong password':
                print('wrong password, connection closed')
                client.close()
                break
            
            
            else:
                print(message)
        except:
            #close connection when error occurs
            if not client._closed:
                print("An error occured!")
            break
#now lets define the write function, which will handle sending messages from the user to the server
def write():
    while True:
        message = input("")
        if message.strip().upper() == "BYE":
            client.send("BYE".encode('utf-8'))
            client.close()
            break
        client.send(f'{nickname}: {message}'.encode('utf-8'))
#to allow simultaneous sending and receiving of messages we need to run the receive and write functions in seperate threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
