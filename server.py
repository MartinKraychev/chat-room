import json
import socket
import threading


def broadcast(message):
    for client in clients:
        client.send(message.encode(config['encoding_type']))


def handle(client):
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
    print('Server is running...')
    while True:
        client, address = server.accept()
        client.send(config['nickname_code'].encode(config['encoding_type']))
        nickname = client.recv(1024).decode(config['encoding_type'])
        clients.append(client)
        nicknames.append(nickname)

        print(f'{nickname} with address {address} joined the chat!')
        broadcast(f'{nickname} with address {address} joined the chat!')

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['host'], config['port']))
    server.listen()
    clients = []
    nicknames = []

    receive()
