# Simple Chat Socket

Uma aplicação de chat simples utilizando sockets em Python para a disciplina de Redes de Computadores 1.

## Como funciona?

**Parte 0: O que é um Socket?**

Um Socket é um meio de conexão entre dois dispositivos na mesma rede, agindo como uma porta de entrada e saída entre os dispositivos.

Sockets possuem três partes: 
- O endereço IP do dispositivo;
- O número da porta;
- O protocolo usado (ex. TCP);

Com esses três componentes, um socket está pronto para conectar o dispositivo com outra máquina em sua rede (desde que ela também possua um socket).

**Parte 1: Inicialização do Servidor**

O arquivo `server.py` é responsável por criar um servidor de chat que aceita conexões de múltiplos clientes.

A criação do servidor é feita utilizando a biblioteca `socket` do python, e a inicialização é feita logo no início da `main()`:

```python
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
```

É inicializada a variável `server` utilizando a função `socket` da biblioteca `socket` (uau kkkk), com os seguintes parâmetros:

- `socket.AF_INET`, que especifica a utilização de **IPv4** para comunicações;
- `socket.SOCK_STREAM`, que especifica o protocolo **TCP** para o socket;

Depois, é "bindado" ao servidor um endereço **HOST** e uma porta **PORT** (ex: 127.0.0.1 e 12345) por meio da função `bind()`.

Por último, o servidor começa a escutar conexões nesse endereço e porta via função `listen()`.

**Parte 2: Aceitando conexões**

Após a inicialização do servidor, é iniciado um loop infinito que aguarda conexões externas ao endereço do servidor:

```python
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)

    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
```

A função `accept()` vem da biblioteca socket, e justamenta espera conexões externas e, ao ter sucesso, retorna uma tupla de valores, o socket do cliente e o endereço de IP do cliente, onde atribuímos respectivamente a **client_socket** e **addr**.

Após uma conexão sucedida, adicionamos o **client_socket** à lista de clientes, para futuro gerenciamento, depois associamos uma `Thread`, usando a  biblioteca `threading`, à uma instância da função criada `handle_client()`, passando **client_socket** como argumento:

```python
thread = threading.Thread(target=handle_client, args=(client_socket,))
```

E por último, a thread é inicializada, utilizando a função `start()` da biblioteca.

#### **Parte 3: Recebimento e envio de mensagens**

Agora com uma instância da função `handle_client()` rodando para cada cliente, elas serão responsáveis por tratar o envio e recebimento de mensagens:

```python
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break
    client_socket.close()
    clients.remove(client_socket)
```

A lógica da função é simples:

Dentro de um loop infinito, o servidor tenta receber mensagens daquele cliente via função `recv(1024)` da biblioteca `socket`, onde **1024** é o tamanho máximo da mensagem (1 KB).

Se a mensagem enviada pelo cliente não for válida, houver algum erro/exceção, o cliente é desconectado, o socket do cliente é fechado e removido da lista de clientes conectados.

Se a mensagem enviada pelo cliente for válida, ela é repassada para outros clientes presentes na lista de clientes, por meio da função criada `broadcast()`.

```python
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

```

A função `broadcast()` é responsável por enviar a mensagem recebida de um cliente para todos os outros que estão conectados, exceto o próprio remetente. Portando, ela recebe como argumentos a mensagem a ser transmitida **message** e o socket do cliente remetente **sender_socket**.

Se algum cliente estiver desconectado ou causar erro durante o envio, o servidor fecha sua conexão e remove esse cliente da lista. 

**Parte 4: Cliente**

O arquivo `client.py` é o responsavel por criar uma "entidade" cliente, que vai se conectar com o servidor (`server.py`).
 
A conexão com o servidor é feita da seguinte maneira:

```python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
```

O recebimento de mensagens é feito pela thread:

```python
thread = threading.Thread(target=receive_messages, args=(client,))
thread.start()
```

Essa thread é uma instância da função `receive_messages()`:

```python
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
```

Essa thread fica ativa paralelamente, escutando mensagens do servidor e imprimindo-as no console.

O envio de mensagens pela parte do cliente é feito com o seguinte código:

```python
message = input()
client.send(f"{username}: {message}".encode('utf-8'))
```

Quando a mensagem é enviada, ela não vai diretamente para outros clientes: Ela é formatada (`utf-8`) e então passada para o servidor, que faz broadcast para todos os outros clientes (Ver [Parte 3](#parte-3-recebimento-e-envio-de-mensagens)).

Quando o usuário deseja sair do chat, basta digitar "/sair": 

```python
if message.lower() == '/sair':
    client.close()
```

## Como testar?

Para subir e testar a aplicação é muito simples, basta rodar o servidor e quantos clientes você quiser.

**Passo a passo:**

1. Abra um terminal e rode o servidor:

    ```bash
    python server.py
    ```

2. Abra outros terminais e rode quantos clientes quiser:

    ```bash
    python client.py
    ```

É isso! Você pode subir quantos clientes quiser para testar, sinta-se a vontade.

Alternativamente, se você estiver no Windows, você pode simplesmente rodar no terminal:

```bash
run_chat_script.bat
```

Desta forma, será automaticamente inicializado 3 terminais, 1 com servidor e 2 com clientes.
