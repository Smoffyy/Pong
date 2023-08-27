import pygame
import random, os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Pygame
pygame.init()

# Access environment variables with default values
WIDTH = int(os.environ.get("WIDTH", 800))
HEIGHT = int(os.environ.get("HEIGHT", 600))
PADDLE_WIDTH = int(os.environ.get("PADDLE_WIDTH", 15))
PADDLE_HEIGHT = int(os.environ.get("PADDLE_HEIGHT", 100))
BALL_SIZE = int(os.environ.get("BALL_SIZE", 20))
PADDLE_SPEED = int(os.environ.get("PADDLE_SPEED", 5))
BALL_SPEED_X = int(os.environ.get("BALL_SPEED_X", 5))
BALL_SPEED_Y = int(os.environ.get("BALL_SPEED_Y", 5))
BALL_SPEED_INCREASE = float(os.environ.get("BALL_SPEED_INCREASE", 0.0001))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Create paddles and ball
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

clock = pygame.time.Clock()

# AI Opponent movement
def move_opponent():
    if ball_speed[0] > 0:  # Only move when the ball is coming towards the opponent
        if opponent_paddle.centery < ball.centery:
            opponent_paddle.y += PADDLE_SPEED
        elif opponent_paddle.centery > ball.centery:
            opponent_paddle.y -= PADDLE_SPEED

# AI Player movement
def move_player_ai():
    if ball_speed[0] < 0:  # Only move when the ball is coming towards the player AI
        if player_paddle.centery < ball.centery:
            player_paddle.y += PADDLE_SPEED
        elif player_paddle.centery > ball.centery:
            player_paddle.y -= PADDLE_SPEED

# Create font for displaying text
font = pygame.font.Font(None, 36)
player_ai_enabled = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player_ai_enabled = not player_ai_enabled

    keys = pygame.key.get_pressed()
    if not player_ai_enabled:
        if keys[pygame.K_UP]:
            player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            player_paddle.y += PADDLE_SPEED

    # Player AI Movement
    if player_ai_enabled:
            move_player_ai()

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed[0] = -ball_speed[0]

    move_opponent()

    # Increase ball speed over time
    ball_speed[0] *= (1 + BALL_SPEED_INCREASE)
    ball_speed[1] *= (1 + BALL_SPEED_INCREASE)

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    if player_ai_enabled:
        text = font.render("Player AI Enabled", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
