import socket
import threading

# Server setup
HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print("Server started... Waiting for connections")

# Broadcast function
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left the chat!".encode('utf-8'))
            usernames.remove(username)
            break

# Accept connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("USERNAME".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        usernames.append(username)
        clients.append(client)

        print(f"Username: {username}")
        broadcast(f"{username} joined the chat!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        receive()