# File: agency_day5.py
import pygame

W_LENGTH = 600
W_HEIGHT = 450
LINE_PX = 3
PLAYER_SIZE = 32
GRAVITY = 700
JUMP_VELOCITY = 400
MOVE_SPEED = 200

pygame.init()
screen = pygame.display.set_mode((W_LENGTH, W_HEIGHT))
clock = pygame.time.Clock()
is_running = True
delta = 0

character = pygame.image.load("Images/Placeholder.png")
x_pos = (W_LENGTH - PLAYER_SIZE) // 2
y_pos = (W_HEIGHT - PLAYER_SIZE) // 2
fall_speed = 0
is_grounded = False

level_file = open("Data/level1.csv", "r")
level_data = level_file.read().rstrip().split("\n")
level_file.close()
level = []
for line in level_data:
    dims = line.split(",")
    level.append(pygame.Rect(int(dims[0]), \
    int(dims[1]), int(dims[2]), int(dims[3])))

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    screen.fill("#B8B8B8")
    for terrain in level:
        pygame.draw.rect(screen, "#B80000", terrain)
        pygame.draw.rect(screen, "#000000", terrain, width=LINE_PX)
    screen.blit(character, (x_pos, y_pos))
    keys = pygame.key.get_pressed()

    if is_grounded:
        is_grounded = False
        for terrain in level:
            if (y_pos + PLAYER_SIZE == terrain.top \
            and x_pos + PLAYER_SIZE > terrain.left \
            and x_pos < terrain.right):
                is_grounded = True
                break

    if not is_grounded:
        fall_speed += GRAVITY * delta
        y_pos += fall_speed * delta
        for terrain in level:
            if (y_pos + PLAYER_SIZE >= terrain.top \
            and y_pos < terrain.top
            and x_pos + PLAYER_SIZE > terrain.left \
            and x_pos < terrain.right):
                is_grounded = True
                fall_speed = 0
                y_pos = terrain.top - PLAYER_SIZE

    if keys[pygame.K_LEFT]:
        x_pos -= MOVE_SPEED * delta
        for terrain in level:
            if (x_pos < terrain.right \
            and x_pos + PLAYER_SIZE > terrain.right \
            and y_pos < terrain.bottom \
            and y_pos + PLAYER_SIZE > terrain.top):
                x_pos = terrain.right
                break

    if keys[pygame.K_SPACE] and is_grounded:
        is_grounded = False
        fall_speed = -JUMP_VELOCITY
        y_pos += fall_speed * delta

    if keys[pygame.K_RIGHT]:
        x_pos += MOVE_SPEED * delta
        for terrain in level:
            if (x_pos + PLAYER_SIZE > terrain.left \
            and x_pos < terrain.left \
            and y_pos < terrain.bottom \
            and y_pos + PLAYER_SIZE > terrain.top):
                x_pos = terrain.left - PLAYER_SIZE
                break

    pygame.display.flip()
    delta = clock.tick(30) / 1000

pygame.quit()
