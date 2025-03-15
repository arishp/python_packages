import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

while True:
    move = input("Your move (0-8): ")
    client_socket.send(move.encode())

    move = client_socket.recv(1024).decode()
    print(f"Opponent chose: {move}")
