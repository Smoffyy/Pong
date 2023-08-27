import pygame
import random
import time
import os
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

# Initialize game objects and variables
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

clock = pygame.time.Clock()

# Initialize scores and reset variables
player_score = 0
opponent_score = 0
reset_start_time = 0
ball_moving = False

# AI Opponent movement
def move_opponent():
    if ball_speed[0] > 0:  # Only move when the ball is coming towards the opponent
        if ball.centery > opponent_paddle.centery:
            opponent_paddle.y += PADDLE_SPEED
        elif ball.centery < opponent_paddle.centery:
            opponent_paddle.y -= PADDLE_SPEED

# AI Player movement
def move_player_ai():
    if ball_speed[0] < 0:  # Only move when the ball is coming towards the player AI
        if ball.centery > player_paddle.centery:
            player_paddle.y += PADDLE_SPEED
        elif ball.centery < player_paddle.centery:
            player_paddle.y -= PADDLE_SPEED

# Reset the ball's position and direction
def reset_ball():
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed[0] = random.choice([-1, 1]) * BALL_SPEED_X
    ball_speed[1] = random.choice([-1, 1]) * BALL_SPEED_Y

# Main game loop
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

    # Opponent AI Movement
    move_opponent()

    # Initialize ball's random direction on the first run
    if ball_speed[0] == BALL_SPEED_X and ball_speed[1] == BALL_SPEED_Y:
        ball_speed[0] = random.choice([-1, 1]) * BALL_SPEED_X
        ball_speed[1] = random.choice([-1, 1]) * BALL_SPEED_Y

    # Handle ball reset and delay
    if ball_moving:
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

    time_since_reset = time.time() - reset_start_time
    if time_since_reset < 1:  # Delay the ball movement for 1 second
        ball_moving = False  # Stop ball movement
    else:
        ball_moving = True  # Start ball movement

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with walls (scoring)
    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
        reset_start_time = time.time()  # Record the time when the ball is reset
        ball_moving = False  # Stop ball movement
    elif ball.right >= WIDTH:
        player_score += 1
        reset_ball()
        reset_start_time = time.time()  # Record the time when the ball is reset
        ball_moving = False  # Stop ball movement

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

    # Draw scores
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(f"Player: {player_score}", True, WHITE)
    opponent_score_text = font.render(f"Opponent: {opponent_score}", True, WHITE)
    screen.blit(player_score_text, (10, 10))
    screen.blit(opponent_score_text, (WIDTH - opponent_score_text.get_width() - 10, 10))

    if player_ai_enabled:
        text = font.render("Player AI Enabled", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(120)

pygame.quit()