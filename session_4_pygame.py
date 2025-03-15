import pygame

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set title
pygame.display.set_caption("Hello, World! - Pygame")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load font
font = pygame.font.Font(None, 50)

# Render text
text = font.render("Hello, World!", True, BLACK)

# Main loop
running = True
while running:
    # Fill screen with white background
    screen.fill(WHITE)

    # Draw text at the center
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
