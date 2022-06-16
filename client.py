import json
import socket
import threading


def receive():
    """
    Receive thread.
    Try to receive a message and if a error occurs, close the socket.
    The first message from the server should always be the nickname code word and we return our nickname as response.
    """
    while True:
        try:
            message = client.recv(1024).decode(config['encoding_type'])
            if message == config['nickname_code']:
                client.send(nickname.encode(config['encoding_type']))
            else:
                print(message)
        except:
            print('Error has occurred')
            client.close()
            break


def send():
    """
    Send thread.
    Try to send a message and if a error occurs, close the socket.
    """
    while True:
        message = input()
        try:
            client.send(f'{nickname}: {message}'.encode(config['encoding_type']))

        except:
            print('Error has occurred')
            client.close()
            break


if __name__ == '__main__':
    # On start loads  constants from the config file and makes the initial socket setup
    with open('config.json', 'r') as f:
        config = json.load(f)

    nickname = input('Enter your nickname: ')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config['host'], config['port']))

    # Defines 2 threads - one for sending and one for listening.
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()
