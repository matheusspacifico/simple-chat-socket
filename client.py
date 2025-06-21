import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\r{message}")
        except:
            print("Conexão encerrada.")
            sock.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    username = input("Digite seu nome: ")
    client.send(f"{username.upper()} entrou no chat.".encode('utf-8'))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        message = input("VOCÊ: ")
        if message.lower() == '/sair':
            client.close()
            break
        full_message = f"{username.upper()}: {message}"
        client.send(full_message.encode('utf-8'))

        # Apaga o input escrito no console para facilitar a leitura
        sys.stdout.write('\033[F')  # Move cursor uma linha acima
        sys.stdout.write('\033[K')  # Limpa a linha
        print(f"VOCÊ: {message}")

if __name__ == "__main__":
    main()
