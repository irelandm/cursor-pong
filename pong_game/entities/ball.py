import pygame
import math
import random
from pong_game.utils.constants import (
    WIDTH, HEIGHT, BALL_RADIUS, INITIAL_BALL_SPEED,
    BALL_SPEED_INCREASE, MAX_BOUNCE_ANGLE, WHITE, PADDLE_HEIGHT
)


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
        """Increase ball speed while maintaining its current direction."""
        self.speed += BALL_SPEED_INCREASE
        # Update dx and dy while preserving their signs
        dx_sign = 1 if self.dx > 0 else -1
        dy_sign = 1 if self.dy > 0 else -1
        self.dx = self.speed * dx_sign
        self.dy = self.speed * dy_sign

    def draw(self, screen):
        """Draw the ball on the screen."""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)

    def get_rect(self):
        """Return a rect for collision detection."""
        return pygame.Rect(
            self.x - BALL_RADIUS,
            self.y - BALL_RADIUS,
            BALL_RADIUS * 2,
            BALL_RADIUS * 2
        )

    def handle_paddle_collision(self, paddle):
        """Handle collision with paddle and calculate new direction.

        Args:
            paddle: The paddle object to check collision with.

        Returns:
            bool: True if collision occurred, False otherwise.
        """
        if self.get_rect().colliderect(paddle.rect):
            # Calculate relative intersection point
            relative_intersect_y = (
                (paddle.rect.centery - self.y) / (PADDLE_HEIGHT / 2)
            )
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
        """Check if a point was scored.

        Returns:
            str or None: 'left' or 'right' indicating scorer, None if no score.
        """
        if self.x - BALL_RADIUS <= 0:
            return 'right'
        elif self.x + BALL_RADIUS >= WIDTH:
            return 'left'
        return None
