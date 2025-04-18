import pygame
import sys
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 7
PADDLE_SPEED = 7
INITIAL_BALL_SPEED = 3
BALL_SPEED_INCREASE = 0.5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_COLOR = (0, 255, 0)
WINNING_SCORE = 3
MAX_BOUNCE_ANGLE = 75  # Maximum angle in degrees

# Game state class
class GameState:
    def __init__(self):
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        self.winner = None
    
    def update_score(self, is_left_scorer):
        if is_left_scorer:
            self.left_score += 1
            if self.left_score >= WINNING_SCORE:
                self.game_over = True
                self.winner = "Left Player"
        else:
            self.right_score += 1
            if self.right_score >= WINNING_SCORE:
                self.game_over = True
                self.winner = "Right Player"
        return self.game_over
    
    def reset(self):
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        self.winner = None

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        
    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
            
        # Keep paddle within screen bounds
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PADDLE_HEIGHT))
        
    def draw(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)

# Ball class
class Ball:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = INITIAL_BALL_SPEED
        self.dx = self.speed * random.choice([1, -1])
        self.dy = self.speed * random.choice([1, -1])
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off top and bottom
        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.dy *= -1
            
    def increase_speed(self):
        # Increase speed while maintaining direction
        self.speed += BALL_SPEED_INCREASE
        # Update dx and dy while preserving their signs
        dx_sign = 1 if self.dx > 0 else -1
        dy_sign = 1 if self.dy > 0 else -1
        self.dx = self.speed * dx_sign
        self.dy = self.speed * dy_sign
            
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)
        
    def get_rect(self):
        # Return a rect for collision detection
        return pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, 
                          BALL_RADIUS * 2, BALL_RADIUS * 2)
    
    def handle_paddle_collision(self, paddle):
        """Handle collision with paddle and calculate new direction"""
        if self.get_rect().colliderect(paddle.rect):
            # Calculate relative intersection point
            relative_intersect_y = (paddle.rect.centery - self.y) / (PADDLE_HEIGHT / 2)
            # Constrain the intersection point to [-1, 1]
            relative_intersect_y = max(-1, min(1, relative_intersect_y))
            # Calculate bounce angle (in radians)
            bounce_angle = relative_intersect_y * math.radians(MAX_BOUNCE_ANGLE)
            
            # Set new direction
            if self.x < WIDTH // 2:  # Left paddle
                self.dx = self.speed * math.cos(bounce_angle)
                self.dy = -self.speed * math.sin(bounce_angle)
            else:  # Right paddle
                self.dx = -self.speed * math.cos(bounce_angle)
                self.dy = -self.speed * math.sin(bounce_angle)
            
            return True
        return False

    def check_scoring(self):
        """Check if a point was scored and return the scorer (None, 'left', or 'right')"""
        if self.x - BALL_RADIUS <= 0:
            return 'right'
        elif self.x + BALL_RADIUS >= WIDTH:
            return 'left'
        return None

if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    
    # Create the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    
    # Create game objects
    game_state = GameState()
    left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()
    
    # Font setup
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_state.game_over:
                if event.key == pygame.K_r:
                    game_state.reset()
                    ball.reset()
                
        if not game_state.game_over:
            # Handle paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                left_paddle.move(up=True)
            if keys[pygame.K_s]:
                left_paddle.move(up=False)
            if keys[pygame.K_UP]:
                right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                right_paddle.move(up=False)
                
            # Move ball
            ball.move()
            
            # Ball collision with paddles
            if ball.handle_paddle_collision(left_paddle) or ball.handle_paddle_collision(right_paddle):
                ball.increase_speed()
            
            # Check scoring
            scorer = ball.check_scoring()
            if scorer:
                game_state.update_score(scorer == 'left')
                ball.reset()
        
        # Draw everything
        screen.fill(BLACK)
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)
        
        # Draw scores
        left_text = font.render(str(game_state.left_score), True, WHITE)
        right_text = font.render(str(game_state.right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 20))
        screen.blit(right_text, (3 * WIDTH // 4, 20))
        
        # Draw game over message
        if game_state.game_over:
            game_over_text = font.render(f"{game_state.winner} Wins!", True, WHITE)
            restart_text = small_font.render("Press R to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit() 