import pygame
import random
import math

# initialize pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# Change Title
pygame.display.set_caption("pyGame Fun")

# Change icon
icon = pygame.image.load("old_yoda.jpg")
pygame.display.set_icon(icon)

# Player IMG
playIMG = pygame.image.load("player.png")
playIMG = pygame.transform.scale(playIMG, (50, 50))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy Orange IMG (Multiple enemies)
enemyOrangeIMG = []
orangeX = []
orangeY = []
orangeX_change = []
orangeY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    initial_enem_img = pygame.image.load("enemy.png")
    enemyOrangeIMG.append(pygame.transform.scale(initial_enem_img, (70, 70)))
    orangeX.append(random.randint(0, 730))  # orange randomly appear on screen
    orangeY.append(random.randint(50, 150))
    orangeX_change.append(4)
    orangeY_change.append(40)

# Friendly IMG (Multiple)
friendlyIMG = []
friendlyX = []
friendlyY = []
friendlyX_change = []
friendlyY_change = []
num_of_friendly = 5

for j in range(num_of_friendly):
    initial_frind_img = pygame.image.load("friendly.png")
    friendlyIMG.append(pygame.transform.scale(initial_frind_img, (70, 70)))
    friendlyX.append(random.randint(0, 730))  # orange randomly appear on screen
    friendlyY.append(random.randint(50, 150))
    friendlyX_change.append(4)
    friendlyY_change.append(40)

# Background IMG
backgroundIMG = pygame.image.load("background.jpg")
backgroundIMG = pygame.transform.scale(backgroundIMG, (800, 600))

# Bullet IMG
bulletIMG = pygame.image.load("bullet.png")
bulletIMG = pygame.transform.scale(bulletIMG, (15, 15))
bulletX = 0  # changing X in while loop
bulletY = 480  # Same Y as the player
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

score = 0


def player(x, y):
    screen.blit(playIMG, (x, y))


def enemyOrange(x, y, i):
    screen.blit(enemyOrangeIMG[i], (x, y))


def friendly(x, y, i):
    screen.blit(friendlyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 25, y + 25))  # Bullet appears at the center of the space ship


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    if distance < 30:
        return True
    else:
        return False


# Properly turn off program
running = True
while running:
    screen.fill((0, 0, 0))  # RGB
    screen.blit(backgroundIMG, (0, 0))  # Background IMG display
    for event in pygame.event.get():  # loop through all events received
        if event.type == pygame.QUIT:  # if QUIT is detected, then quit
            running = False

        # If keystroke is pressed, check if it is left or right or space
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # Only register to fire when the state if ready
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change

    # Prevent out of bound
    if playerX < 0:
        playerX = 0
    if playerX > 750:
        playerX = 750

    # Orange movement
    for i in range(num_of_enemies):
        orangeX[i] += orangeX_change[i]

        if orangeX[i] < 0:
            orangeX_change[i] = 3
            orangeY[i] += orangeY_change[i]
        if orangeX[i] > 730:
            orangeX_change[i] = -3
            orangeY[i] += orangeY_change[i]

        # Collision detection
        enemy_collision = isCollision(orangeX[i], orangeY[i],
                                bulletX, bulletY)  # Return True or False
        if enemy_collision:
            bulletY = 480  # reset the bullet location
            bullet_state = "ready"  # reset bullet state
            score += 1
            print(score)
            orangeX[i] = random.randint(0, 730)  # orange randomly appear on screen
            orangeY[i] = random.randint(0, 200)
        enemyOrange(orangeX[i], orangeY[i], i)

    #friendly movement
    for i in range(num_of_friendly):
        friendlyX[i] += friendlyX_change[i]

        if friendlyX[i] < 0:
            friendlyX_change[i] = 3
            friendlyY[i] += friendlyY_change[i]
        if friendlyX[i] > 730:
            friendlyX_change[i] = -3
            friendlyY[i] += friendlyY_change[i]

        # Collision detection
        friendly_collision = isCollision(friendlyX[i], friendlyY[i],
                                bulletX, bulletY)  # Return True or False
        if friendly_collision:  # GAME OVER
            for l in range(num_of_friendly):
                friendlyY[l] = 5000
            for p in range(num_of_enemies):
                orangeY[p] = 5000
            break
        friendly(orangeX[i], orangeY[i], i)

    # Bullet movement
    if bulletY <= -70:  # If the bullet reaches the top, reset it
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    pygame.display.update()
