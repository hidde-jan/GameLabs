import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PADDLE_START_X = 10
PADDLE_START_Y = 20

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

OTHER_PADDLE_START_X = SCREEN_WIDTH - PADDLE_WIDTH - PADDLE_START_X

BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
other_paddle_rect = pygame.Rect((OTHER_PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Line
line_rect = pygame.Rect((SCREEN_WIDTH / 2 - 2, 10), (4, SCREEN_HEIGHT - 20))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
other_score = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Load the paddle sound.
paddle_sound = pygame.mixer.Sound('paddle.wav')
bounce_sound = pygame.mixer.Sound('v_bounce.wav')
point_sound = pygame.mixer.Sound('point.wav')

# Game loop
while True:
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
            pygame.quit()
        # Control the paddle with the mouse
        elif event.type == pygame.MOUSEMOTION:
            paddle_rect.centery = event.pos[1]
            # correct paddle position if it's going out of window
            if paddle_rect.top < 0:
                paddle_rect.top = 0
            elif paddle_rect.bottom >= SCREEN_HEIGHT:
                paddle_rect.bottom = SCREEN_HEIGHT

    # This test if up or down keys are pressed; if yes, move the paddle
    if pygame.key.get_pressed()[pygame.K_w] and paddle_rect.top > 0:
        paddle_rect.top -= BALL_SPEED
    elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect.bottom < SCREEN_HEIGHT:
        paddle_rect.top += BALL_SPEED
    if pygame.key.get_pressed()[pygame.K_UP] and other_paddle_rect.top > 0:
        other_paddle_rect.top -= BALL_SPEED
    elif pygame.key.get_pressed()[pygame.K_DOWN] and other_paddle_rect.bottom < SCREEN_HEIGHT:
        other_paddle_rect.top += BALL_SPEED
    elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit(0)
        pygame.quit()

    # Update ball position
    ball_rect.left += ball_speed[0]
    ball_rect.top += ball_speed[1]

    # Test if the ball hits an edge.
    if ball_rect.left <= 0:
        other_score += 1
    elif ball_rect.right >= SCREEN_WIDTH:
        score += 1

    # Ball collision with rails
    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
        ball_speed[1] = -ball_speed[1]
        bounce_sound.play()

    if ball_rect.right >= SCREEN_WIDTH or ball_rect.left <= 0:
        ball_speed[0] = -ball_speed[0]
        ball_rect.left = SCREEN_WIDTH / 2
        ball_rect.top = SCREEN_HEIGHT / 2
        point_sound.play()

    # Test if the ball is hit by the paddle; if yes reverse speed.
    if paddle_rect.colliderect(ball_rect) or other_paddle_rect.colliderect(ball_rect):
        ball_speed[0] = -ball_speed[0]
        paddle_sound.play()

    # Clear screen
    screen.fill((255, 255, 255))

    # Render the ball, the paddle, and the score
    pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
    pygame.draw.rect(screen, (0, 0, 0), other_paddle_rect) # Other paddle

    pygame.draw.rect(screen, (255, 0, 0), line_rect) # Line

    pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball

    score_text = font.render(str(score), True, (0, 0, 0))
    screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score

    other_score_text = font.render(str(other_score), True, (0, 0, 0))
    screen.blit(other_score_text, (int(SCREEN_WIDTH * 0.75) - font.size(str(other_score))[0] / 2, 5)) # The score

    # Update screen and wait 20 milliseconds
    pygame.display.flip()
    pygame.time.delay(20)
