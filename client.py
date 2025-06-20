import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Conexão encerrada.")
            sock.close()
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Digite seu nome: ")
client.send(f"{username} entrou no chat.".encode('utf-8'))

thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()

while True:
    message = input()
    if message.lower() == '/sair':
        client.close()
        break
    client.send(f"{username}: {message}".encode('utf-8'))
