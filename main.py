import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion Simulation")

font_large = pygame.font.Font(None, 36)
font_medium = pygame.font.Font(None, 28)

running = True
while running:
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 20, WIDTH, 20))
    pygame.draw.circle(screen, RED, (WIDTH - 50, HEIGHT - 50), 10)

    title = font_large.render("Projectile Motion Simulation", True, BLACK)
    screen.blit(title, (20, 20))

    instruction1 = font_medium.render("Press 'Q' or close window to quit", True, BLACK)
    instruction2 = font_medium.render("Adjust simulation in subsequent stages", True, BLACK)
    screen.blit(instruction1, (20, 70))
    screen.blit(instruction2, (20, 100))

    pygame.draw.line(screen, BLUE, (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50), 2)
    pygame.draw.line(screen, BLUE, (50, HEIGHT - 100), (50, HEIGHT - 50), 2)

    pygame.draw.rect(screen, GREEN, (50, 150, 200, 50))
    button_text = font_medium.render("Start Simulation", True, WHITE)
    screen.blit(button_text, (60, 160))

    pygame.draw.rect(screen, BLUE, (50, 250, 200, 20))
    pygame.draw.rect(screen, RED, (50, 240, 10, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()
