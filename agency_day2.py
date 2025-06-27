# File: agency_day2.py
import pygame

W_LENGTH = 600
W_HEIGHT = 450
RAD = 16

pygame.init()
screen = pygame.display.set_mode((W_LENGTH, W_HEIGHT))
clock = pygame.time.Clock()
is_running = True
delta = 0

character = pygame.image.load("Images/PixelGarchomp.png")
player = pygame.Rect(W_LENGTH / 2 - RAD, W_HEIGHT / 2 - RAD, RAD * 2, RAD * 2)

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    screen.fill("#B8B8B8")
    screen.blit(character, player)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_h]:
        player.move_ip(-300 * delta, 0)
    if keys[pygame.K_j]:
        player.move_ip(0, 300 * delta)
    if keys[pygame.K_k]:
        player.move_ip(0, -300 * delta)
    if keys[pygame.K_l]:
        player.move_ip(300 * delta, 0)

    pygame.display.flip()
    delta = clock.tick(30) / 1000

pygame.quit()
