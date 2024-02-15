import socket

# Задаем хост и порт сервера
host = input("Введите имя хоста (по умолчанию localhost): ") or 'localhost'
port = int(input("Введите номер порта (по умолчанию 12345): ") or 12345)

# Создаем сокет TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect((host, port))
print(f'Подключение к серверу {host}:{port}...')

# Отправляем начальное сообщение без имени клиента
client_socket.sendall("".encode())
data = client_socket.recv(1024)
print(f'Ответ от сервера: {data.decode()}')

while True:
    # Вводим сообщение
    message = input("Введите сообщение: ")
    print(f'Сообщение - {message} - отправлено на сервер')

    # Если сообщение exit, отключаемся
    if message == "exit":
        break

    # Отправляем сообщение на сервер
    client_socket.sendall(message.encode())

    # Читаем ответ от сервера
    data = client_socket.recv(1024)
    print(f'Ответ от сервера: {data.decode()}')

# Закрываем соединение с сервером
client_socket.close()
print('Подключение закрыто.')