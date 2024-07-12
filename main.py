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
air_resistance = 0.05

x, y = 50, HEIGHT - 50
vx = velocity * math.cos(math.radians(angle))
vy = -velocity * math.sin(math.radians(angle))

trajectory_points = []

paused = False
start_time = 0
pause_time = 0

# Slider constants
SLIDER_WIDTH = 200
SLIDER_HEIGHT = 10
SLIDER_COLOR = GREEN
SLIDER_DRAG_COLOR = BLUE

def draw_slider(x, y, value, max_value, label):
    pygame.draw.rect(screen, WHITE, (x, y, SLIDER_WIDTH, SLIDER_HEIGHT))
    pygame.draw.rect(screen, SLIDER_COLOR, (x, y, int(SLIDER_WIDTH * (value / max_value)), SLIDER_HEIGHT))

    font_label = font_medium.render(label, True, BLACK)
    screen.blit(font_label, (x, y - 25))

def update_slider(x, y, value, max_value):
    mx, my = pygame.mouse.get_pos()
    if x <= mx <= x + SLIDER_WIDTH and y <= my <= y + SLIDER_HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            value = (mx - x) / SLIDER_WIDTH * max_value
    return value

def draw_buttons():
    pygame.draw.rect(screen, GREEN, (50, 400, 200, 30))
    start_button_text = font_medium.render("Start Simulation", True, WHITE)
    screen.blit(start_button_text, (60, 405))

    pygame.draw.rect(screen, BLUE, (50, 450, 200, 30))
    reset_button_text = font_medium.render("Reset Simulation", True, WHITE)
    screen.blit(reset_button_text, (60, 455))

    pygame.draw.rect(screen, RED, (300, 400, 150, 30))
    pause_button_text = font_medium.render("Pause / Resume", True, WHITE)
    screen.blit(pause_button_text, (310, 405))

def draw_info():
    info_text = font_medium.render(f"Position: ({x:.1f}, {y:.1f})", True, BLACK)
    screen.blit(info_text, (20, 350))

    velocity_text = font_medium.render(f"Velocity: ({vx:.1f}, {vy:.1f})", True, BLACK)
    screen.blit(velocity_text, (20, 380))

def reset_simulation():
    global x, y, vx, vy, trajectory_points
    x, y = 50, HEIGHT - 50
    vx = velocity * math.cos(math.radians(angle))
    vy = -velocity * math.sin(math.radians(angle))
    trajectory_points = []

running = True
while running:
    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 20, WIDTH, 20))
    pygame.draw.circle(screen, RED, (WIDTH - 50, HEIGHT - 50), 10)

    title = font_large.render("Projectile Motion Simulation", True, BLACK)
    screen.blit(title, (20, 20))

    instruction1 = font_medium.render("Press 'Q' or close window to quit", True, BLACK)
    instruction2 = font_medium.render("Adjust simulation parameters:", True, BLACK)
    instruction3 = font_medium.render(f"Angle: {angle:.1f} degrees", True, BLACK)
    instruction4 = font_medium.render(f"Velocity: {velocity:.1f} pixels/frame", True, BLACK)
    instruction6 = font_medium.render(f"Simulation Speed: {simulation_speed:.1f}x", True, BLACK)
    instruction7 = font_medium.render(f"Air Resistance: {air_resistance:.2f}", True, BLACK)
    instruction8 = font_medium.render(f"Gravity: {gravity:.2f}", True, BLACK)
    screen.blit(instruction1, (20, 70))
    screen.blit(instruction2, (20, 100))
    screen.blit(instruction3, (20, 130))
    screen.blit(instruction4, (20, 160))
    screen.blit(instruction6, (20, 220))
    screen.blit(instruction7, (20, 250))
    screen.blit(instruction8, (20, 280))

    pygame.draw.line(screen, BLUE, (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50), 2)
    pygame.draw.line(screen, BLUE, (50, HEIGHT - 100), (50, HEIGHT - 50), 2)

    # Draw sliders
    angle = update_slider(600, 90, angle, 90)
    velocity = update_slider(600, 140, velocity, 50)
    simulation_speed = update_slider(600, 190, simulation_speed, 5)
    air_resistance = update_slider(600, 240, air_resistance, 0.1)
    gravity = update_slider(600, 290, gravity, 1.0)

    draw_slider(600, 90, angle, 90, "Angle:")
    draw_slider(600, 140, velocity, 50, "Velocity:")
    draw_slider(600, 190, simulation_speed, 5, "Simulation Speed:")
    draw_slider(600, 240, air_resistance, 0.1, "Air Resistance:")
    draw_slider(600, 290, gravity, 1.0, "Gravity:")

    draw_buttons()
    draw_info()

    if not paused:
        if x >= 50 and y <= HEIGHT - 50:
            trajectory_points.append((int(x), int(y)))

            if len(trajectory_points) > 1000:  # Limit trajectory points for performance
                trajectory_points.pop(0)

            for i in range(int(simulation_speed)):
                x += vx
                y += vy
                vy += gravity / simulation_speed
                vx *= (1 - air_resistance)

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
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 50 <= mx <= 250 and 400 <= my <= 430:
                if not paused:
                    paused = True
                else:
                    paused = False
            elif 50 <= mx <= 250 and 450 <= my <= 480:
                reset_simulation()
            elif 300 <= mx <= 450 and 400 <= my <= 430:
                paused = not paused

    pygame.display.flip()

pygame.quit()
