import pygame
import socket
import threading

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Remote Game Server")

player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5

def handle_client(client_socket):
    global player_x, player_y
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data == "left":
                player_x -= player_speed
            elif data == "right":
                player_x += player_speed
            elif data == "up":
                player_y -= player_speed
            elif data == "down":
                player_y += player_speed
        except ConnectionResetError:
            break
    client_socket.close()

def game_loop():
    global player_x, player_y
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

    server_socket.close()

game_thread = threading.Thread(target=game_loop)
game_thread.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0), (player_x, player_y), 20)
    pygame.display.flip()

pygame.quit()