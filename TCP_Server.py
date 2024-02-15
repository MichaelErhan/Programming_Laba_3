import socket
import datetime

# Задаем хост и порт сервера
host = input("Введите имя хоста (по умолчанию localhost): ") or 'localhost'
port = int(input("Введите номер порта (по умолчанию 12345): ") or 12345)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        server_socket.bind((host, port))
        print(f"Сервер успешно запущен на порту {port}")
        break
    except socket.error:
        print(f"Порт {port} занят, подключаемся к свободному порту...")
        port += 1

server_socket.listen()


# Открываем лог-файл для записи служебных сообщений
log_file = open("server_log.txt", "a")

# Функция для записи служебных сообщений в лог-файл
def write_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"[{timestamp}] {message}\n")
    log_file.flush()  # Принудительно сохраняем запись в файл

# Функция для проверки, известен ли клиент по IP-адресу
def check_client(ip_address):
    with open("clients.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().split(",")[0] == ip_address:
                return True
    return False

# Функция для записи нового клиента в файл
def write_client(ip_address, name, password):
    with open("clients.txt", "a") as file:
        file.write(f"{ip_address},{name},{password}\n")

def handle_connection(client_socket, client_address):
    ip_address = client_address[0]
    if check_client(ip_address):
        # Известный клиент, приветствуем по имени
        with open("clients.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip().split(",")[0] == ip_address:
                    name = line.strip().split(",")[1]
        write_log(f"Приветствуем клиента {name} с IP-адресом {ip_address}")
        client_socket.send(f"Привет, {name}!".encode())
    else:
        # Новый клиент, запрашиваем имя
        client_socket.send("Привет! Как тебя зовут? ".encode())
        name = client_socket.recv(1024).decode()

        # Пароль клиента
        client_socket.send("Придумай пароль: ".encode())
        password = client_socket.recv(1024).decode()

        write_client(ip_address, name, password)
        write_log(f"Добавлен новый клиент {name} с IP-адресом {ip_address} и паролем {password}")
        client_socket.send(f"Приятно познакомиться, {name}!".encode())

    # Бесконечный цикл для принятия и отправки сообщений
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                write_log(f"Получено сообщение от клиента {name}: {message}")
                client_socket.send(message.encode())
                write_log(f"Отправлено сообщение клиенту {name}: {message}")
            else:
                # Клиент отключился
                write_log(f"Клиент {name} с IP-адресом {ip_address} отключился")
                break
        except ConnectionResetError:
            # Клиент внезапно отключился
            write_log(f"Клиент {name} с IP-адресом {ip_address} внезапно отключился")
            break


write_log(f'Сервер запущен на хосте {host}...')
write_log(f'Сервер начал прослушивать порт {port}...')

while True:
    # Принимаем входящее соединение
    client_socket, client_address = server_socket.accept()
    write_log(f"Получено новое подключение от {client_address[0]}:{client_address[1]}")
    handle_connection(client_socket, client_address)