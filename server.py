import json
import socket
import threading


def broadcast(message):
    """
    Sends messages to all connected clients
    """
    for client in clients:
        client.send(message.encode(config['encoding_type']))


def handle(client):
    """
    Tries to receive a message from a client and if a message occurs, it removes it from the list and closes the connection.
    """
    while True:
        try:
            message = client.recv(1024).decode(config['encoding_type'])
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)

            print(f"{nickname} left the chat!")
            broadcast(f"{nickname} left the chat!")
            break


def receive():
    """
    Waiting for clients to connects and adds them and their nicknames to predefined lists.
    """
    print('Server is running...')
    while True:
        client, address = server.accept()
        # Once client is connected it sends it a nickname keyword and expects a response with nickname.
        client.send(config['nickname_code'].encode(config['encoding_type']))
        nickname = client.recv(1024).decode(config['encoding_type'])

        clients.append(client)
        nicknames.append(nickname)

        print(f'{nickname} with address {address} joined the chat!')
        broadcast(f'{nickname} with address {address} joined the chat!')

        # For every new client it adds a new thread to listen for messages.
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == '__main__':
    # On start loads the constants from the config file.
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Does the initial setup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['host'], config['port']))
    server.listen()
    clients = []
    nicknames = []

    receive()
