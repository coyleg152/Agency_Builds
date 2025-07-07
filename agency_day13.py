# File: agency_day13.py
import pygame

W_LENGTH = 600
W_HEIGHT = 450
LINE_PX = 3
P_LENGTH = 14
P_HEIGHT = 32
MAX_FRAME_DELAY = 2
GRAVITY = 900
JUMP_VELOCITY = 425
MOVE_SPEED = 160

STARTING_LEVEL = "Data/level1-1.csv"
STARTING_X = 173
STARTING_Y = 328

pygame.init()
screen = pygame.display.set_mode((W_LENGTH, W_HEIGHT))
clock = pygame.time.Clock()
is_running = True
delta = 0.0

character = pygame.image.load("Images/CrystalWalking.png")
animation = 0
anim_frame = 0
frame_delay = MAX_FRAME_DELAY
x_pos = STARTING_X
y_pos = STARTING_Y
fall_speed = 0
is_grounded = False

level = []
planks = []
cells = []
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
    planks.clear()
    cells.clear()
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
        elif data[0] == "plank":
            planks.append(pygame.Rect(int(data[1]), \
            int(data[2]), int(data[3]), int(data[4])))
        elif data[0] == "cell":
            cells.append(pygame.Rect(int(data[1]), \
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

left_load, left_x, left_y, right_load, right_x, right_y \
= load_level(STARTING_LEVEL)

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    screen.fill("#B8B8B8")
    for cell in cells:
        pygame.draw.rect(screen, "#808080", cell)
    screen.blit(character, (x_pos, y_pos), \
    (P_LENGTH * anim_frame, P_HEIGHT * animation, P_LENGTH , P_HEIGHT))
    for terrain in level:
        pygame.draw.rect(screen, "#B80000", terrain)
        pygame.draw.rect(screen, "#000000", terrain, width=LINE_PX)
    for plank in planks:
        pygame.draw.rect(screen, "#804000", plank)
        pygame.draw.rect(screen, "#000000", plank, width=LINE_PX)
    keys = pygame.key.get_pressed()

    if is_grounded:
        is_grounded = False
        for platform in (level + planks):
            if (y_pos + P_HEIGHT == platform.top \
            and x_pos + P_LENGTH > platform.left \
            and x_pos < platform.right):
                is_grounded = True
                break

    if not is_grounded:
        fall_speed += GRAVITY * delta
        y_pos += fall_speed * delta
        if y_pos > W_HEIGHT:
            game_over = pygame.image.load("Images/GameOver.png")
            screen.blit(game_over, (W_LENGTH // 2 - 99, W_HEIGHT // 2 - 54))
            pygame.display.flip()

            while is_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    left_load, left_x, left_y, right_load, right_x, right_y \
                    = load_level(STARTING_LEVEL)
                    x_pos = STARTING_X
                    y_pos = STARTING_Y
                    break
                delta = clock.tick(30) / 1000

        if fall_speed > 0:
            for platform in (level + planks):
                if (y_pos + P_HEIGHT >= platform.top \
                and y_pos < platform.top
                and x_pos + P_LENGTH > platform.left \
                and x_pos < platform.right):
                    is_grounded = True
                    fall_speed = 0
                    y_pos = platform.top - P_HEIGHT

        if fall_speed < 0:
            for terrain in level:
                if (y_pos <= terrain.bottom \
                and y_pos + P_HEIGHT > terrain.bottom
                and x_pos + P_LENGTH > terrain.left \
                and x_pos < terrain.right):
                    fall_speed *= -0.5
                    y_pos = terrain.bottom

    if keys[pygame.K_LEFT]:
        x_pos -= MOVE_SPEED * delta
        animation = 1
        if frame_delay < 1:
            anim_frame = (anim_frame + 1) % 4
            frame_delay = MAX_FRAME_DELAY
        else:
            frame_delay -= 1

        if x_pos < 0 and left_load != "X":
            x_pos = left_x
            y_pos = left_y
            left_load, left_x, left_y, right_load, right_x, right_y \
            = load_level(left_load)
            continue

        for terrain in level:
            if (x_pos < terrain.right \
            and x_pos + P_LENGTH > terrain.right \
            and y_pos < terrain.bottom \
            and y_pos + P_HEIGHT > terrain.top):
                x_pos = terrain.right
                break

    if keys[pygame.K_RIGHT]:
        x_pos += MOVE_SPEED * delta
        animation = 0
        if frame_delay < 1:
            anim_frame = (anim_frame + 1) % 4
            frame_delay = MAX_FRAME_DELAY
        else:
            frame_delay -= 1

        if x_pos + P_LENGTH > W_LENGTH and right_load != "X":
            x_pos = right_x
            y_pos = right_y
            left_load, left_x, left_y, right_load, right_x, right_y \
            = load_level(right_load)
            continue

        for terrain in level:
            if (x_pos + P_LENGTH > terrain.left \
            and x_pos < terrain.left \
            and y_pos < terrain.bottom \
            and y_pos + P_HEIGHT > terrain.top):
                x_pos = terrain.left - P_LENGTH
                break

    if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) \
    or (not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]):
        anim_frame = 0
        frame_delay = MAX_FRAME_DELAY

    if keys[pygame.K_SPACE] and is_grounded:
        is_grounded = False
        fall_speed = -JUMP_VELOCITY
        y_pos += fall_speed * delta

    if keys[pygame.K_UP] and is_grounded:
        for cell in cells:
            if (x_pos + 4 > cell.left and x_pos + P_LENGTH < cell.right + 4 \
            and y_pos > cell.top and y_pos + P_HEIGHT < cell.bottom + 4):
                x_pos = cell.left + cell.width // 2 - P_LENGTH // 2
                animation = 2
                anim_frame = 0

    pygame.display.flip()
    delta = clock.tick(30) / 1000

pygame.quit()
