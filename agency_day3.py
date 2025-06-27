# File: agency_day3.py
import pygame

W_LENGTH = 600
W_HEIGHT = 450
GRAVITY = 300
JUMP_VELOCITY = 300

pygame.init()
screen = pygame.display.set_mode((W_LENGTH, W_HEIGHT))
clock = pygame.time.Clock()
is_running = True
delta = 0

character = pygame.image.load("Images/PixelGarchomp.png")
x_pos = W_LENGTH // 2 - 16
y_pos = W_HEIGHT // 2 - 16
ground = pygame.Rect(0, 4 * W_HEIGHT // 5, W_LENGTH, W_HEIGHT // 5)
fall_speed = 0
is_grounded = False

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    screen.fill("#B8B8B8")
    pygame.draw.rect(screen, "#B80000", ground)
    pygame.draw.rect(screen, "#000000", ground, width=3)
    screen.blit(character, (x_pos, y_pos))
    keys = pygame.key.get_pressed()

    if not is_grounded:
        fall_speed += GRAVITY * delta
        y_pos += fall_speed * delta
        if (y_pos + 32 >= 4 * W_HEIGHT // 5):
            is_grounded = True
            fall_speed = 0
            y_pos = 4 * W_HEIGHT // 5 - 32

    if keys[pygame.K_LEFT]:
        x_pos -= 300 * delta
    if keys[pygame.K_SPACE] and is_grounded:
        is_grounded = False
        fall_speed = -JUMP_VELOCITY
        y_pos += fall_speed * delta
    if keys[pygame.K_RIGHT]:
        x_pos += 300 * delta

    pygame.display.flip()
    delta = clock.tick(30) / 1000

pygame.quit()
