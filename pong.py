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
TICK_RATE = int(os.environ.get("TICK_RATE", 60))
RESET_TIME = float(os.environ.get("RESET_TIME", 1.0))
BALL_SPEED_INCREASE = float(os.environ.get("BALL_SPEED_INCREASE", 0.0001))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
batch_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Initialize game objects and variables
class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

player_paddle = GameObject(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
opponent_paddle = GameObject(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
ball = GameObject(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE, WHITE)

game_state = {
    "player_score": 0,
    "opponent_score": 0,
    "reset_start_time": 0,
    "ball_moving": False,
    "player_ai_enabled": False
}

ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

clock = pygame.time.Clock()

# AI Opponent movement
def move_opponent():
    if ball_speed[0] > 0:  # Only move when the ball is coming towards the opponent
        if ball.rect.centery > opponent_paddle.rect.centery and opponent_paddle.rect.bottom < HEIGHT:
            opponent_paddle.move(0, PADDLE_SPEED)
        elif ball.rect.centery < opponent_paddle.rect.centery and opponent_paddle.rect.top > 0:
            opponent_paddle.move(0, -PADDLE_SPEED)

# AI Player movement
def move_player_ai():
    if game_state["player_ai_enabled"] and ball_speed[0] < 0:
        if ball.rect.centery > player_paddle.rect.centery:
            player_paddle.move(0, PADDLE_SPEED)
        elif ball.rect.centery < player_paddle.rect.centery:
            player_paddle.move(0, -PADDLE_SPEED)

# Reset the ball's position and direction
def reset_ball():
    ball.rect.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed[0] = random.choice([-1, 1]) * BALL_SPEED_X
    ball_speed[1] = random.choice([-1, 1]) * BALL_SPEED_Y

def predict_ball_trajectory(ball_rect, ball_speed, num_frames):
    """
    Predicts the trajectory of the ball based on its current position and speed.

    Args:
        ball_rect (pygame.Rect): The current rectangle representing the ball's position.
        ball_speed (list): The current speed of the ball in the x and y directions.
        num_frames (int): The number of frames to predict ahead.

    Returns:
        list: A list of predicted (x, y) positions of the ball for the specified number of frames.
    """
    predicted_positions = []
    x, y = ball_rect.center
    dx, dy = ball_speed

    for _ in range(num_frames):
        x += dx
        y += dy
        predicted_positions.append((x, y))

    return predicted_positions

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_state["player_ai_enabled"] = not game_state["player_ai_enabled"]

    keys = pygame.key.get_pressed()
    if not game_state["player_ai_enabled"]:
        if keys[pygame.K_UP] and player_paddle.rect.top > 0:
            player_paddle.move(0, -PADDLE_SPEED)
        if keys[pygame.K_DOWN] and player_paddle.rect.bottom < HEIGHT:
            player_paddle.move(0, PADDLE_SPEED)

    # Player AI Movement
    if game_state["player_ai_enabled"]:
        move_player_ai()

    # Opponent AI Movement
    move_opponent()

    # Initialize ball's random direction on the first run
    if ball_speed[0] == BALL_SPEED_X and ball_speed[1] == BALL_SPEED_Y:
        ball_speed[0] = random.choice([-1, 1]) * BALL_SPEED_X
        ball_speed[1] = random.choice([-1, 1]) * BALL_SPEED_Y

    # Handle ball reset and delay
    if game_state["ball_moving"]:
        ball.rect.x += ball_speed[0]
        ball.rect.y += ball_speed[1]

    time_since_reset = time.time() - game_state["reset_start_time"]
    if time_since_reset < RESET_TIME:  # Delay the ball movement for a set amount of time
        game_state["ball_moving"] = False  # Stop ball movement
    else:
        game_state["ball_moving"] = True  # Start ball movement

    # Ball collision with walls
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with walls (scoring)
    if ball.rect.left <= 0:
        game_state["opponent_score"] += 1
        reset_ball()
        game_state["reset_start_time"] = time.time()  # Record the time when the ball is reset
        game_state["ball_moving"] = False  # Stop ball movement
    elif ball.rect.right >= WIDTH:
        game_state["player_score"] += 1
        reset_ball()
        game_state["reset_start_time"] = time.time()  # Record the time when the ball is reset
        game_state["ball_moving"] = False  # Stop ball movement

    # Ball collision with paddles
    if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(opponent_paddle.rect):
        ball_speed[0] = -ball_speed[0]

    # Increase ball speed over time
    ball_speed[0] *= (1 + BALL_SPEED_INCREASE)
    ball_speed[1] *= (1 + BALL_SPEED_INCREASE)

    # Batch drawing onto the batch_surface
    batch_surface.fill(BLACK)
    player_paddle.draw(batch_surface)
    opponent_paddle.draw(batch_surface)
    pygame.draw.ellipse(batch_surface, WHITE, ball.rect)  # Draw the ball as an ellipse
    pygame.draw.aaline(batch_surface, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Update the screen with the batch drawing
    screen.blit(batch_surface, (0, 0))

    # Draw scores and text directly onto the screen
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(f"Player: {game_state['player_score']}", True, WHITE)
    opponent_score_text = font.render(f"Opponent: {game_state['opponent_score']}", True, WHITE)
    screen.blit(player_score_text, (10, 10))
    screen.blit(opponent_score_text, (WIDTH - opponent_score_text.get_width() - 10, 10))

    if game_state["player_ai_enabled"]:
        text = font.render("Player AI Enabled", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 10))

    num_frames = TICK_RATE // 4  # Number of frames to predict ahead divided by a certain number. (Helps with performance)

    # Predict ball trajectories for the opponent and player AI
    opponent_predicted_positions = predict_ball_trajectory(opponent_paddle.rect, ball_speed, num_frames)
    player_ai_predicted_positions = predict_ball_trajectory(player_paddle.rect, ball_speed, num_frames)

    # Draw prediction lines for the opponent's trajectory
    for pos in opponent_predicted_positions:
        pygame.draw.line(batch_surface, (0, 255, 0), ball.rect.center, pos, 2)

    # Draw prediction lines for the player AI's trajectory
    for pos in player_ai_predicted_positions:
        pygame.draw.line(batch_surface, (0, 0, 255), ball.rect.center, pos, 2)

    pygame.display.flip()
    clock.tick_busy_loop(TICK_RATE)

pygame.quit()