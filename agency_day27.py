# File: agency_day27.py
import pygame
from enemies import PrisonGuard
from objects import SpikeTrap
from objects import Checkpoint

W_LENGTH = 600
W_HEIGHT = 450
FRAMERATE = 30
LINE_PX = 3
SIGHTLINE_ON_FRAMES = 24
SIGHTLINE_OFF_FRAMES = 6

P_LENGTH = 14
P_HEIGHT = 32
MAX_FRAME_DELAY = 2
GRAVITY = 900
JUMP_VELOCITY = 425
MOVE_SPEED = 160

def get_startpos(filename):
    level_file = open(filename, "r")
    level_data = level_file.read().rstrip().split("\n")
    level_file.close()
    start_x = 0
    start_y = 0
    for line in level_data:
        data = line.split(",")
        if data[0] == "start":
            start_x = int(data[1])
            start_y = int(data[2])
            break
    return start_x, start_y
    
pygame.init()
screen = pygame.display.set_mode((W_LENGTH, W_HEIGHT))
clock = pygame.time.Clock()
is_running = True
is_gameover = False
delta = 0.0

bg_image = pygame.image.load("Images/TitleScreen.png")
screen.blit(bg_image, (0, 0, W_LENGTH, W_HEIGHT))
pygame.display.flip()
pygame.mixer.music.load("Audio/AgencyTitle.ogg")
pygame.mixer.music.play()

while is_running:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        is_running = False
    if keys[pygame.K_SPACE]:
        break
    delta = clock.tick(FRAMERATE) / 1000

starting_level = "Data/level1-1.csv"
character = pygame.image.load("Images/CrystalWalking.png")
animation = 0
anim_frame = 0
frame_delay = MAX_FRAME_DELAY
x_pos, y_pos = get_startpos(starting_level)
fall_speed = 0
is_grounded = False
is_hidden = False

flag = Checkpoint()
flag.level = "Data/level1-3.csv"
flag.length = 20
flag.height = 36

enemy_image = pygame.image.load("Images/PrisonGuard.png")
enemy_length = 14
enemy_height = 28
enemy_vh = 14
enemy_speed = 80
sightline_on = True
sightline_delay = SIGHTLINE_ON_FRAMES

terrain_image = pygame.image.load("Images/PrisonTerrain.png")
bg_image = pygame.image.load("Images/PrisonBG.png")
level = []
planks = []
cells = []
spikes = []
enemies = []
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
    spikes.clear()
    enemies.clear()
    flag.visible = False
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
        elif data[0] == "spike":
            spikes.append(SpikeTrap(int(data[1]), int(data[2]), \
            int(data[3]), int(data[4]), int(data[5]), \
            float(data[6]), float(data[7])))
        elif data[0] == "guard":
            enemies.append(PrisonGuard(int(data[1]), int(data[2]), \
            int(data[3]), int(data[4]), int(data[5]), \
            int(data[6]), int(data[7])))
        elif data[0] == "flag":
            flag.x = int(data[1])
            flag.y = int(data[2])
            flag.visible = True
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
= load_level(starting_level)
pygame.mixer.music.stop()
pygame.mixer.music.load("Audio/ThePrisoner.ogg")
pygame.mixer.music.play()

def draw_flag(screen, flag, LINE_PX):
    if flag.activated:
        pygame.draw.polygon(screen, "#00FFFF", \
        ((flag.x + flag.length // 2, flag.y), \
        (flag.x + flag.length, flag.y + flag.height // 2), \
        (flag.x + flag.length // 2, flag.y + flag.height), \
        (flag.x, flag.y + flag.height // 2)))
        pygame.draw.polygon(screen, "#00C0FF", \
        ((flag.x + flag.length // 2, flag.y), \
        (flag.x + flag.length, flag.y + flag.height // 2), \
        (flag.x + flag.length // 2, flag.y + flag.height), \
        (flag.x, flag.y + flag.height // 2)), width=LINE_PX)
    else:
        pygame.draw.polygon(screen, "#0000C0", \
        ((flag.x + flag.length // 2, flag.y), \
        (flag.x + flag.length, flag.y + flag.height // 2), \
        (flag.x + flag.length // 2, flag.y + flag.height), \
        (flag.x, flag.y + flag.height // 2)))
        pygame.draw.polygon(screen, "#000080", \
        ((flag.x + flag.length // 2, flag.y), \
        (flag.x + flag.length, flag.y + flag.height // 2), \
        (flag.x + flag.length // 2, flag.y + flag.height), \
        (flag.x, flag.y + flag.height // 2)), width=LINE_PX)

def draw_spikes(screen, spike, LINE_PX):
    offset = spike.length // 8
    if spike.state == 0:
        for i in range(4):
            pygame.draw.polygon(screen, "#606060", \
            ((spike.x + offset * 2 * i, spike.y + spike.height), \
            (spike.x + offset * 2 * i + offset, spike.y), \
            (spike.x + offset * 2 * (i + 1), spike.y + spike.height)))
    else:
        for i in range(4):
            pygame.draw.polygon(screen, "#E00000", \
            ((spike.x + offset * 2 * i, spike.y + spike.height), \
            (spike.x + offset * 2 * i + offset, spike.y), \
            (spike.x + offset * 2 * (i + 1), spike.y + spike.height)))
            pygame.draw.polygon(screen, "#000000", \
            ((spike.x + offset * 2 * i, spike.y + spike.height), \
            (spike.x + offset * 2 * i + offset, spike.y), \
            (spike.x + offset * 2 * (i + 1), spike.y + spike.height)), \
            width=LINE_PX)

while is_running:
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    screen.blit(bg_image, (0, 0, W_LENGTH, W_HEIGHT))
    if flag.visible:
        draw_flag(screen, flag, LINE_PX)
    for spike in spikes:
        draw_spikes(screen, spike, LINE_PX)
    for cell in cells:
        pygame.draw.rect(screen, "#404040", cell)
    if is_hidden:
        screen.blit(character, (x_pos, y_pos), \
        (P_LENGTH * anim_frame, P_HEIGHT * animation, P_LENGTH , P_HEIGHT))
    for cell in cells:
        pygame.draw.rect(screen, "#606060", cell, width=LINE_PX)
    if not is_hidden:
        screen.blit(character, (x_pos, y_pos), \
        (P_LENGTH * anim_frame, P_HEIGHT * animation, P_LENGTH , P_HEIGHT))
    if sightline_on:
        for enemy in enemies:
            if enemy.direction == 1:
                pygame.draw.rect(screen, "#FFFF80", \
                (enemy.x + enemy_length, enemy.y, \
                enemy.r_sight - enemy.x - enemy_length, enemy_vh))
            else:
                pygame.draw.rect(screen, "#FFFF80", (enemy.l_sight, \
                enemy.y, enemy.x - enemy.l_sight, enemy_vh))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy.x, enemy.y), \
        (enemy_length * enemy.anim_frame, enemy_height * enemy.animation, \
        enemy_length, enemy_height))
    for terrain in level:
        screen.blit(terrain_image, terrain, \
        (0, 0, terrain.width, terrain.height))
        pygame.draw.rect(screen, "#000000", terrain, width=LINE_PX)
    for plank in planks:
        pygame.draw.rect(screen, "#804000", plank)
        pygame.draw.rect(screen, "#000000", plank, width=LINE_PX)
    keys = pygame.key.get_pressed()

    if is_gameover:
        pygame.mixer.music.stop()
        game_over = pygame.image.load("Images/GameOver.png")
        screen.blit(game_over, (W_LENGTH // 2 - 99, W_HEIGHT // 2 - 54))
        pygame.display.flip()

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                is_running = False
            if keys[pygame.K_r]:
                left_load, left_x, left_y, right_load, right_x, right_y \
                = load_level(starting_level)
                x_pos, y_pos = get_startpos(starting_level)
                pygame.mixer.music.play()
                is_gameover = False
                break
            delta = clock.tick(FRAMERATE) / 1000

    if keys[pygame.K_SPACE] and is_grounded:
        if is_hidden:
            is_hidden = False
            animation = 0
            anim_frame = 0
            frame_delay = MAX_FRAME_DELAY
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
                is_hidden = True
                break

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

        if fall_speed > 0:
            for platform in (level + planks):
                if (y_pos + P_HEIGHT >= platform.top \
                and y_pos + P_HEIGHT - fall_speed * delta <= platform.top \
                and x_pos + P_LENGTH > platform.left \
                and x_pos < platform.right):
                    is_grounded = True
                    fall_speed = 0
                    y_pos = platform.top - P_HEIGHT

        if fall_speed < 0:
            for terrain in level:
                if (y_pos <= terrain.bottom \
                and y_pos + P_HEIGHT > terrain.bottom \
                and x_pos + P_LENGTH > terrain.left \
                and x_pos < terrain.right):
                    fall_speed *= -0.4
                    y_pos = terrain.bottom

        if y_pos > W_HEIGHT:
            is_gameover = True

    if keys[pygame.K_LEFT]:
        x_pos -= MOVE_SPEED * delta
        animation = 1
        is_hidden = False
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
        is_hidden = False
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

    sightline_delay -= 1
    if sightline_delay <= 0:
        sightline_on = not sightline_on
        if sightline_on:
            sightline_delay = SIGHTLINE_ON_FRAMES
        else:
            sightline_delay = SIGHTLINE_OFF_FRAMES

    if flag.visible and not flag.activated:
        if x_pos < flag.x + flag.length and x_pos + P_LENGTH > flag.x \
        and y_pos < flag.y + flag.height and y_pos + P_HEIGHT > flag.y:
            starting_level = flag.level
            flag.activated = True

    for spike in spikes:
        spike.delay -= delta
        if spike.delay <= 0.0:
            spike.state = (spike.state + 1) % 2
            spike.delay = spike.max_delay
        if spike.state == 1 \
        and x_pos < spike.x + spike.length and x_pos + P_LENGTH > spike.x \
        and y_pos < spike.y + spike.height and y_pos + P_HEIGHT > spike.y:
            is_gameover = True

    for enemy in enemies:
        enemy.x += enemy.direction * enemy_speed * delta
        if enemy.x < enemy.l_bound:
            enemy.x = enemy.l_bound
            enemy.direction = 1
            enemy.animation = 0
        if enemy.x + enemy_length > enemy.r_bound:
            enemy.x = enemy.r_bound - enemy_length
            enemy.direction = -1
            enemy.animation = 1
        if enemy.frame_delay < 1:
            enemy.frame_delay = enemy.MAX_FRAME_DELAY
            enemy.anim_frame = (enemy.anim_frame + 1) % 2
        else:
            enemy.frame_delay -= 1

        if y_pos < enemy.y + enemy_vh and y_pos + P_HEIGHT > enemy.y \
        and not is_hidden:
            if (enemy.direction == -1 and x_pos < enemy.x \
            and x_pos + P_LENGTH > enemy.l_sight) or (enemy.direction == 1 \
            and x_pos + P_LENGTH > enemy.x + enemy_length \
            and x_pos < enemy.r_sight):
                sightline_on = True
                is_gameover = True
        
    pygame.display.flip()
    delta = clock.tick(FRAMERATE) / 1000

pygame.mixer.music.stop()
pygame.quit()
