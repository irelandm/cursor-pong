import pygame
import sys
from pong_game.entities.ball import Ball
from pong_game.entities.paddle import Paddle
from pong_game.entities.game_state import GameState
from pong_game.utils.constants import (
    WIDTH, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT,
    FPS, WHITE, BLACK
)


class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()

        self.ball = Ball()
        self.left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.game_state = GameState()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Left paddle movement
        if keys[pygame.K_w]:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s]:
            self.left_paddle.move(up=False)

        # Right paddle movement
        if keys[pygame.K_UP]:
            self.right_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            self.right_paddle.move(up=False)

    def update(self):
        self.ball.move()

        # Check for paddle collisions
        if (self.ball.handle_paddle_collision(self.left_paddle) or
                self.ball.handle_paddle_collision(self.right_paddle)):
            self.ball.increase_speed()

        # Check for scoring
        scorer = self.ball.check_scoring()
        if scorer:
            if scorer == 'left':
                self.game_state.update_score(True)
            else:
                self.game_state.update_score(False)
            self.ball.reset()

    def draw(self):
        self.screen.fill(BLACK)

        # Draw game objects
        self.ball.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)

        # Draw scores
        font = pygame.font.Font(None, 74)
        left_score = font.render(str(self.game_state.left_score), True, WHITE)
        right_score = font.render(str(self.game_state.right_score), True, WHITE)
        self.screen.blit(left_score, (WIDTH // 4, 20))
        self.screen.blit(right_score, (3 * WIDTH // 4, 20))

        # Draw game over message
        if self.game_state.game_over:
            game_over = font.render(f"{self.game_state.winner} Wins!", True, WHITE)
            restart = font.render("Press R to Restart", True, WHITE)
            self.screen.blit(
                game_over,
                (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 2)
            )
            self.screen.blit(
                restart,
                (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 60)
            )

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_r and
                      self.game_state.game_over):
                    self.game_state.reset()
                    self.ball.reset()

            if not self.game_state.game_over:
                self.handle_input()
                self.update()

            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = PongGame()
    game.run()
