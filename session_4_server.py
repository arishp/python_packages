import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 12345))
server_socket.listen(1)
print("Waiting for a player to join...")

player_socket, addr = server_socket.accept()
print(f"Player connected from {addr}")

board = [" "]*9

def print_board():
    print("\n" + "\n".join([" | ".join(board[i:i+3]) for i in range(0, 9, 3)]) + "\n")

while True:
    print_board()
    move = player_socket.recv(1024).decode()
    board[int(move)] = "X"

    if " " not in board:
        print_board()
        print("Game over!")
        break

    move = input("Your move (0-8): ")
    board[int(move)] = "O"
    player_socket.send(move.encode())

player_socket.close()
server_socket.close()
