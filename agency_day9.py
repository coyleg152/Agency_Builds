# File: agency_day9.py
import pygame

W_LENGTH = 600
W_HEIGHT = 450
LINE_PX = 3
PLAYER_SIZE = 32
GRAVITY = 750
JUMP_VELOCITY = 400
MOVE_SPEED = 200

pygame.init()
screen = pygame.display.set_mode((W_LENGTH, W_HEIGHT))
clock = pygame.time.Clock()
is_running = True
delta = 0

character = pygame.image.load("Images/Placeholder.png")
x_pos = 269
y_pos = 328
fall_speed = 0
is_grounded = False
is_gameover = False

level = []
left_load = "X"
left_x = 0
left_y = 0
right_load = "X"
right_x = 0
right_y = 0

def load_level(filename):
    level_file = open(filename, "r")
    level_data = level_file.read().rstrip().split("\n")
    level_file.close()
    level.clear()
    l_file = "X"
    l_x = 0
    l_y = 0
    r_file = "X"
    r_x = 0
    r_y = 0
    for line in level_data:
        data = line.split(",")
        if data[0] == "rect":
            level.append(pygame.Rect(int(data[1]), \
            int(data[2]), int(data[3]), int(data[4])))
        elif data[0] == "left":
            l_file = data[1]
            l_x = int(data[2])
            l_y = int(data[3])
        elif data[0] == "right":
            r_file = data[1]
            r_x = int(data[2])
            r_y = int(data[3])
    return l_file, l_x, l_y, r_file, r_x, r_y

left_load, left_x, left_y, right_load, right_x, right_y = load_level("Data/level1-1.csv")

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
        if y_pos > W_HEIGHT:
            game_over = pygame.image.load("Images/GameOver.png")
            screen.blit(game_over, (W_LENGTH // 2 - 99, W_HEIGHT // 2 - 54))
            is_gameover = True
            is_running = False

        if fall_speed > 0:
            for terrain in level:
                if (y_pos + PLAYER_SIZE >= terrain.top \
                and y_pos < terrain.top
                and x_pos + PLAYER_SIZE > terrain.left \
                and x_pos < terrain.right):
                    is_grounded = True
                    fall_speed = 0
                    y_pos = terrain.top - PLAYER_SIZE

        if fall_speed < 0:
            for terrain in level:
                if (y_pos <= terrain.bottom \
                and y_pos + PLAYER_SIZE > terrain.bottom
                and x_pos + PLAYER_SIZE > terrain.left \
                and x_pos < terrain.right):
                    fall_speed *= -0.5
                    y_pos = terrain.bottom

    if keys[pygame.K_LEFT]:
        x_pos -= MOVE_SPEED * delta
        if x_pos < 0 and left_load != "X":
            x_pos = left_x
            y_pos = left_y
            left_load, left_x, left_y, right_load, right_x, right_y = load_level(left_load)
            continue

        for terrain in level:
            if (x_pos < terrain.right \
            and x_pos + PLAYER_SIZE > terrain.right \
            and y_pos < terrain.bottom \
            and y_pos + PLAYER_SIZE > terrain.top):
                x_pos = terrain.right
                break

    if keys[pygame.K_RIGHT]:
        x_pos += MOVE_SPEED * delta
        if x_pos + PLAYER_SIZE > W_LENGTH and right_load != "X":
            x_pos = right_x
            y_pos = right_y
            left_load, left_x, left_y, right_load, right_x, right_y = load_level(right_load)
            continue

        for terrain in level:
            if (x_pos + PLAYER_SIZE > terrain.left \
            and x_pos < terrain.left \
            and y_pos < terrain.bottom \
            and y_pos + PLAYER_SIZE > terrain.top):
                x_pos = terrain.left - PLAYER_SIZE
                break

    if keys[pygame.K_SPACE] and is_grounded:
        is_grounded = False
        fall_speed = -JUMP_VELOCITY
        y_pos += fall_speed * delta

    pygame.display.flip()
    delta = clock.tick(30) / 1000

if is_gameover:
    clock.tick(0.25)

pygame.quit()
