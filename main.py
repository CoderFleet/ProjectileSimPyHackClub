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

angle = 45
velocity = 20
gravity = 0.4
simulation_speed = 1.0

x, y = 50, HEIGHT - 50
vx = velocity * math.cos(math.radians(angle))
vy = -velocity * math.sin(math.radians(angle))

trajectory_points = []

paused = False
start_time = 0
pause_time = 0

running = True
while running:
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 20, WIDTH, 20))
    pygame.draw.circle(screen, RED, (WIDTH - 50, HEIGHT - 50), 10)

    title = font_large.render("Projectile Motion Simulation", True, BLACK)
    screen.blit(title, (20, 20))

    instruction1 = font_medium.render("Press 'Q' or close window to quit", True, BLACK)
    instruction2 = font_medium.render("Adjust simulation parameters:", True, BLACK)
    instruction3 = font_medium.render(f"Angle: {angle} degrees", True, BLACK)
    instruction4 = font_medium.render(f"Velocity: {velocity} pixels/frame", True, BLACK)
    instruction5 = font_medium.render("Press 'P' to pause/resume", True, BLACK)
    instruction6 = font_medium.render(f"Simulation Speed: {simulation_speed}x", True, BLACK)
    screen.blit(instruction1, (20, 70))
    screen.blit(instruction2, (20, 100))
    screen.blit(instruction3, (20, 130))
    screen.blit(instruction4, (20, 160))
    screen.blit(instruction5, (20, 190))
    screen.blit(instruction6, (20, 220))

    pygame.draw.line(screen, BLUE, (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50), 2)
    pygame.draw.line(screen, BLUE, (50, HEIGHT - 100), (50, HEIGHT - 50), 2)

    pygame.draw.rect(screen, GREEN, (50, 200, 200, 30))
    angle_text = font_medium.render(f"Angle: {angle} degrees", True, WHITE)
    screen.blit(angle_text, (60, 205))

    pygame.draw.rect(screen, GREEN, (50, 250, 200, 30))
    velocity_text = font_medium.render(f"Velocity: {velocity} pixels/frame", True, WHITE)
    screen.blit(velocity_text, (60, 255))

    pygame.draw.rect(screen, BLUE, (50, 300, 200, 30))
    start_button_text = font_medium.render("Start Simulation", True, WHITE)
    screen.blit(start_button_text, (60, 305))

    pygame.draw.rect(screen, BLUE, (50, 350, 200, 30))
    gravity_text = font_medium.render(f"Gravity: {gravity}", True, WHITE)
    screen.blit(gravity_text, (60, 355))

    pygame.draw.rect(screen, GREEN, (50, 400, 200, 30))
    speed_up_text = font_medium.render("Speed Up", True, WHITE)
    screen.blit(speed_up_text, (60, 405))

    pygame.draw.rect(screen, GREEN, (50, 450, 200, 30))
    slow_down_text = font_medium.render("Slow Down", True, WHITE)
    screen.blit(slow_down_text, (60, 455))

    if not paused:
        if x >= 50 and y <= HEIGHT - 50:
            trajectory_points.append((int(x), int(y)))

            if len(trajectory_points) > 1000:
                trajectory_points.pop(0)

            for i in range(int(simulation_speed)):
                x += vx
                y += vy
                vy += gravity / simulation_speed

    pygame.draw.circle(screen, BLACK, (int(x), int(y)), 5)

    for point in trajectory_points:
        pygame.draw.circle(screen, BLUE, point, 2)

    if x >= WIDTH - 50:
        max_height = (velocity ** 2 * (math.sin(math.radians(angle)) ** 2)) / (2 * gravity)
        range_x = (velocity ** 2 * math.sin(math.radians(2 * angle))) / gravity
        info_text1 = font_medium.render(f"Maximum Height: {max_height:.2f} pixels", True, BLACK)
        info_text2 = font_medium.render(f"Range: {range_x:.2f} pixels", True, BLACK)
        screen.blit(info_text1, (20, 490))
        screen.blit(info_text2, (20, 520))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_p:
                if not paused:
                    pause_time = pygame.time.get_ticks()
                    paused = True
                else:
                    start_time += pygame.time.get_ticks() - pause_time
                    paused = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 50 <= mx <= 250 and 200 <= my <= 230:
                angle = (mx - 50) * 90 // 200
                vx = velocity * math.cos(math.radians(angle))
                vy = -velocity * math.sin(math.radians(angle))
            elif 50 <= mx <= 250 and 250 <= my <= 280:
                velocity = (mx - 50) * 50 // 200 + 1
                vx = velocity * math.cos(math.radians(angle))
                vy = -velocity * math.sin(math.radians(angle))
            elif 50 <= mx <= 250 and 300 <= my <= 330:
                x, y = 50, HEIGHT - 50
                vx = velocity * math.cos(math.radians(angle))
                vy = -velocity * math.sin(math.radians(angle))
            elif 50 <= mx <= 250 and 350 <= my <= 380:
                gravity += 0.1
                gravity_text = font_medium.render(f"Gravity: {gravity}", True, WHITE)
                screen.blit(gravity_text, (60, 355))
            elif 50 <= mx <= 250 and 400 <= my <= 430:
                simulation_speed = min(5.0, simulation_speed + 0.1)
                speed_up_text = font_medium.render(f"Speed Up (+): {simulation_speed:.1f}x", True, WHITE)
                screen.blit(speed_up_text, (60, 405))
            elif 50 <= mx <= 250 and 450 <= my <= 480:
                simulation_speed = max(0.1, simulation_speed - 0.1)
                slow_down_text = font_medium.render(f"Slow Down (-): {simulation_speed:.1f}x", True, WHITE)
                screen.blit(slow_down_text, (60, 455))

    pygame.display.flip()

pygame.quit()
