import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Pygame")
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.wav')
BULLET_HIT_SOUND.set_volume(0.1)
BULLET_FIRE_SOUND.set_volume(0.1)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

# events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# spaceships & background
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), -90)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# drawing on screen
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # make background white
    WIN.blit(SPACE, (0, 0))

    # making border
    pygame.draw.rect(WIN, BLACK, BORDER)

    # health
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # spaceship sprites
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # updating display
    pygame.display.update()

# yellow spaceship move
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # 'a' LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < BORDER.x: # 'd' RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # 'w' UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGHT: # 's' DOWN
        yellow.y += VEL

# red spaceship move
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT arrow
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VEL < WIDTH: # RIGHT arrow
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP arrow
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT: # DOWN arrow
        red.y += VEL

# bullet move / hit
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # yellow bullets
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        # collide with red check
        if red.colliderect(bullet):
            # make event for red hit
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        # collide with wall check
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    # red bullets
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        # collide with yellow check
        if yellow.colliderect(bullet):
            # make event for red hit
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        # collide with wall check
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# on win
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    # rectangles that represent sprites
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # game loop
    clock = pygame.time.Clock()
    run = True
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    while run:
        # setting the FPS to 60
        clock.tick(FPS)
        for event in pygame.event.get():
            #when stopping the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # shooting bullets
            if event.type == pygame.KEYDOWN:
                # left control (yellow)
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                # right control (red)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # red hit
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            # yellow hit
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # checking for win
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # which keys are being pressed
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

# checking if file is run
if __name__ == "__main__":
    main()