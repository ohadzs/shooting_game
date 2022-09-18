import pygame
import time
import random
import math
from pygame import mixer
from pygame.locals import *

start = 0

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("img\\bg2.png")

mixer.music.load("img\\bgm2.wav")
mixer.music.play(-1)

pygame.display.set_caption("My First Game")
icon = pygame.image.load("img\\002.png")
pygame.display.set_icon(icon)


startIng = pygame.image.load("img\\start_button.png")
startIng2 = pygame.image.load("img\\start_button_hover.png")
state = 0

playerIng = pygame.image.load("img\\revolverR.png")
playerX = 100
playerY = 100
playerX_change = 0
playerY_change = 0
playerD = "R"


fireballIng = pygame.image.load("img\\fireball.png")
fireballX = random.randint(0, 738)
fireballY = -62
fireballY_change = 7


enemyIng = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyIng.append(pygame.image.load("img\\enemy" + str(random.randint(0, 2)) + ".png"))
    enemyX.append(random.randint(0, 738))
    enemyY.append(random.randint(30, 538))
    d = random.randint(0, 2)
    if d == 0:
        enemyX_change.append(3)
        enemyY_change.append(0)
    else:
        enemyX_change.append(0)
        enemyY_change.append(3)


bulletIng = []
bulletX = []
bulletY = []
bulletX_change = []
bulletY_change = []
bullet_state = []
num_of_bullets = 3
s = []

for i in range(num_of_bullets):
    bulletIng.append(pygame.image.load("img\\bulletR.png"))
    bulletX.append(0)
    bulletY.append(0)
    bulletX_change.append(25)
    bulletY_change.append(5)
    bullet_state.append("ready")
    s.append("R")


score_value1 = 0
go = 0
mone = 0
score_value = 0
font = pygame.font.Font("HealthyWorld.otf", 22)
textX = 10
textY = 10
end = time.time()

over_font = pygame.font.Font("HealthyWorld.otf", 74)

restartIng = pygame.image.load("img\\restart_button.png")
restartIng2 = pygame.image.load("img\\restart_button_hover.png")


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value) +
                        "   |   BULLETS MISSED: " + str(mone - score_value) +
                        "   |   TIME: " + str(int(end - start)),
                        True, (100, 100, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 260))


def player(x, y):
    screen.blit(playerIng, (x, y))


def fireball(x, y):
    screen.blit(fireballIng, (x, y))


def enemy(x, y, e):
    screen.blit(enemyIng[e], (x, y))


def fire_bullet(x, y, b):
    global bullet_state
    global bulletX
    global bulletY
    global bulletX_change
    bullet_state[b] = "fire"
    bulletX[b] = x
    bulletY[b] = y
    if s[b] == "R":
        screen.blit(bulletIng[b], (x + 60, y + 7))
        bulletX_change[b] = 25
        bulletIng[b] = pygame.image.load("img\\bulletR.png")
    if s[b] == "L":
        screen.blit(bulletIng[b], (x, y + 7))
        bulletX_change[b] = -25
        bulletIng[b] = pygame.image.load("img\\bulletL.png")


def is_collision(ex, ey, bx, by):
    distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow((ey + 17) - by, 2)))
    if distance < 30:
        return True
    else:
        return False


def is_collision2(ex, ey, px, py):
    distance = math.sqrt((math.pow(ex - px, 2)) + (math.pow(ey - py, 2)))
    if distance < 32:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (1, 1))

    mx, my = pygame.mouse.get_pos()

    if state == 0:
        screen.blit(startIng, (380, 260))
        if 380 <= mx <= 442 and 260 <= my <= 322:
            screen.blit(startIng2, (380, 260))

        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                running = False

            if event1.type == MOUSEBUTTONDOWN:
                if event1.button == 1 and 380 <= mx <= 442 and 260 <= my <= 322:
                    state = 1
                    start = time.time()

    else:
        screen.blit(restartIng, (758, 10))
        if mx >= 750 and my <= 50:
            screen.blit(restartIng2, (758, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and 750 <= mx <= 800 and 0 <= my <= 50:
                    score_value1 = -2
                    go = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -8
                    playerD = "L"
                    playerIng = pygame.image.load("img\\revolverL.png")
                if event.key == pygame.K_RIGHT:
                    playerX_change = 8
                    playerD = "R"
                    playerIng = pygame.image.load("img\\revolverR.png")
                if event.key == pygame.K_UP:
                    playerY_change = -8
                if event.key == pygame.K_DOWN:
                    playerY_change = 8
                if event.key == pygame.K_SPACE:
                    for bn in range(num_of_bullets):
                        if bullet_state[bn] == "ready":
                            bullet_sound = mixer.Sound("img\\gunshot.wav")
                            bullet_sound.play()
                            s[bn] = playerD
                            fire_bullet(playerX, playerY, bn)
                            mone += 1
                            break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        playerX += playerX_change
        playerY += playerY_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 738:
            playerX = 738
        if playerY <= 0:
            playerY = 0
        elif playerY >= 538:
            playerY = 538

        fireballY += fireballY_change
        if int(start - end) % 5 == 0 and go == 0:
            fireballY = -62
            fireballX = random.randint(0, 738)

        for i in range(num_of_enemies):
            enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY_change[i] = 0
                enemyX[i] = 0
            elif enemyX[i] >= 738:
                enemyX_change[i] = -3
                enemyY_change[i] = 0
                enemyX[i] = 738
            if enemyY[i] <= 0:
                enemyY_change[i] = 3
                enemyX_change[i] = 0
                enemyY[i] = 0
            elif enemyY[i] >= 538:
                enemyY_change[i] = -3
                enemyX_change[i] = 0
                enemyY[i] = 538
            for bn in range(num_of_bullets):
                collision = is_collision(enemyX[i], enemyY[i], bulletX[bn], bulletY[bn])
                if collision:
                    enemy_sound = mixer.Sound("img\\bip.wav")
                    enemy_sound.play()
                    bullet_state[bn] = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, 738)
                    enemyY[i] = random.randint(0, 538)
                    d = random.randint(0, 2)
                    if d == 0:
                        enemyX_change[i] = 3
                        enemyY_change[i] = 0
                    else:
                        enemyX_change[i] = 0
                        enemyY_change[i] = 3
            enemy(enemyX[i], enemyY[i], i)  # maybe move to "point"

            collision2 = is_collision2(enemyX[i], enemyY[i], playerX, playerY)
            collision3 = is_collision2(fireballX, fireballY, playerX, playerY)
            if collision2 or collision3:
                mixer.music.pause()
                game_over_sound = mixer.Sound("img\\game_over_sound.wav")
                game_over_sound.play()
                go = 1
                score_value1 = score_value
                for j in range(num_of_enemies):
                    enemyX_change[j] = 0
                    enemyY_change[j] = 0
                    enemyX[j] = 446
                    enemyY[j] = 253
                break
                # point

        if go == 1:
            game_over_text()
            if score_value1 != score_value:
                game_start_sound = mixer.Sound("img\\game_start_sound.wav")
                game_start_sound.play()
                mixer.music.play(-1)
                for i in range(num_of_enemies):
                    d = random.randint(0, 1)
                    if d == 0:
                        enemyX_change[i] = 3
                        enemyY_change[i] = 0
                    else:
                        enemyX_change[i] = 0
                        enemyY_change[i] = 3
                score_value = 0
                mone = 0
                start = time.time()
                go = 0

        for bn in range(num_of_bullets):
            if bulletX[bn] >= 800 or bulletX[bn] <= 0:
                bullet_state[bn] = "ready"
            if bullet_state[bn] == "fire":
                fire_bullet(bulletX[bn], bulletY[bn], bn)
                bulletX[bn] += bulletX_change[bn]

        fireball(fireballX, fireballY)
        player(playerX, playerY)
        show_score(textX, textY)
        end = time.time()
    pygame.display.update()
