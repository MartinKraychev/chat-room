import json
import socket
import threading


def receive():
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
    while True:
        message = input()
        try:
            client.send(f'{nickname}: {message}'.encode(config['encoding_type']))

        except:
            print('Error has occurred')
            client.close()
            break


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    nickname = input('Enter your nickname: ')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config['host'], config['port']))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()
