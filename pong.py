import pygame
import random
import time
from dotenv import load_dotenv
from pathlib import Path

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
pygame.display.set_caption("Pong")

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Paddle(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.move(0, -self.speed)
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.move(0, self.speed)

class Ball(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def update(self):
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
        self.move(self.speed_x, self.speed_y)

class Game:
    def __init__(self):
        self.paddle = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
        self.opponent_paddle = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
        self.ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE, WHITE)
        self.reset_ball()

    def reset_ball(self):
        self.ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.ball.speed_x = random.choice([-1, 1]) * BALL_SPEED_X
        self.ball.speed_y = random.choice([-1, 1]) * BALL_SPEED_Y

    def update(self):
        if not self.ball.rect.colliderect(self.paddle.rect) and not self.ball.rect.colliderect(self.opponent_paddle.rect):
            if time.time() - self.reset_time > RESET_TIME:
                self.ball.update()
        else:
            self.ball.speed_x *= -1
            self.reset_time = time.time()

    def draw(self, surface):
        surface.fill(BLACK)
        self.paddle.draw(surface)
        self.opponent_paddle.draw(surface)
        self.ball.draw(surface)

# Main game loop
running = True
game = Game()
reset_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game.paddle.speed *= -1

    keys = pygame.key.get_pressed()
    if not keys[pygame.K_q]:
        game.paddle.update()

    game.update()

    num_frames = TICK_RATE // 4
    predicted_positions = [self.ball.rect.center]
    for _ in range(num_frames):
        self.ball.update()
        predicted_positions.append(self.ball.rect.center)

    batch_surface = pygame.Surface((WIDTH, HEIGHT))
    game.draw(batch_surface)
    screen.blit(batch_surface, (0, 0))

    font = pygame.font.Font(None, 36)
    player_score_text = font.render(f"Player: {game.paddle.speed}", True, WHITE)
    opponent_score_text = font.render(f"Opponent: {abs(game.opponent_paddle.rect.centery - game.ball.rect.centery)}", True, WHITE)
    screen.blit(player_score_text, (10, 10))
    screen.blit(opponent_score_text, (WIDTH - opponent_score_text.get_width() - 10, 10))

    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick_busy_loop(TICK_RATE)

pygame.quit()
