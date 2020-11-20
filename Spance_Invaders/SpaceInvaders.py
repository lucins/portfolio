import pygame
import random
import math
from pygame import mixer

# Initialisation of pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))  # screen size in pixels

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('battleship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Displaying score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('spaceship.png'))
    enemyX.append(random.randint(20, 716))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
Bulletimg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 0
BulletX_change = 0
BulletY_change = 10
bullet_state = "ready"  # ready = can't see bullet Fire = bulllet is moving


def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(Bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# keeps window open until exited
running = True
while running:

    screen.fill((0, 0, 65))  # colour of screen in RGB
    screen.blit(background, (0, 0))  # background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE and bullet_state != "fire":
                BulletX = playerX
                BulletY = playerY
                fire_bullet(BulletX, BulletY)
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -2
            if event.key == pygame.K_DOWN:
                playerY_change = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 20:
        playerX = 20
    if playerX >= 716:
        playerX = 716
    if playerY <= 450:
        playerY = 450
    if playerY >= 530:
        playerY = 530

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 20:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 716:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            Explosion_Sound = mixer.Sound('Explosion.wav')
            Explosion_Sound.play()
            BulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(20, 716)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if BulletY <= 0:
        BulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    # collision

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # updates the game screen (do this after every change)
