import pygame
from pong_game.utils.constants import (
    PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, PADDLE_COLOR, HEIGHT
)


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
