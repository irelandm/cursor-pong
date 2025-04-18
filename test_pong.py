import unittest
import pygame
from pong_game.entities.ball import Ball
from pong_game.entities.paddle import Paddle
from pong_game.entities.game_state import GameState
from pong_game.utils.constants import (
    WIDTH, HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT,
    BALL_RADIUS, INITIAL_BALL_SPEED, WINNING_SCORE
)


class TestPongGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game_state = GameState()
        self.ball = Ball()
        self.left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)

    def test_ball_initialization(self):
        """Test ball initialization and properties"""
        self.assertEqual(self.ball.x, WIDTH // 2)
        self.assertEqual(self.ball.y, HEIGHT // 2)
        self.assertEqual(self.ball.speed, INITIAL_BALL_SPEED)
        self.assertTrue(abs(self.ball.dx) == INITIAL_BALL_SPEED)
        self.assertTrue(abs(self.ball.dy) == INITIAL_BALL_SPEED)

    def test_ball_movement(self):
        """Test ball movement and boundary collision"""
        initial_x = self.ball.x
        initial_y = self.ball.y

        # Move ball
        self.ball.move()

        # Check position changed
        self.assertNotEqual(self.ball.x, initial_x)
        self.assertNotEqual(self.ball.y, initial_y)

        # Test top boundary collision
        self.ball.y = BALL_RADIUS
        self.ball.dy = -1
        self.ball.move()
        self.assertGreater(self.ball.dy, 0)  # Should reverse direction

        # Test bottom boundary collision
        self.ball.y = HEIGHT - BALL_RADIUS
        self.ball.dy = 1
        self.ball.move()
        self.assertLess(self.ball.dy, 0)  # Should reverse direction

    def test_ball_speed_increase(self):
        """Test ball speed increase after paddle collision"""
        initial_speed = self.ball.speed
        self.ball.increase_speed()
        self.assertGreater(self.ball.speed, initial_speed)

    def test_paddle_initialization(self):
        """Test paddle initialization and properties"""
        self.assertEqual(self.left_paddle.rect.x, 20)
        self.assertEqual(self.right_paddle.rect.x, WIDTH - 20 - PADDLE_WIDTH)

    def test_paddle_movement(self):
        """Test paddle movement and boundary constraints"""
        # Test upward movement
        initial_y = self.left_paddle.rect.y
        self.left_paddle.move(up=True)
        self.assertLess(self.left_paddle.rect.y, initial_y)

        # Test downward movement
        initial_y = self.left_paddle.rect.y
        self.left_paddle.move(up=False)
        self.assertGreater(self.left_paddle.rect.y, initial_y)

        # Test top boundary
        self.left_paddle.rect.y = 0
        self.left_paddle.move(up=True)
        self.assertEqual(self.left_paddle.rect.y, 0)

        # Test bottom boundary
        self.left_paddle.rect.y = HEIGHT - PADDLE_HEIGHT
        self.left_paddle.move(up=False)
        self.assertEqual(self.left_paddle.rect.y, HEIGHT - PADDLE_HEIGHT)

    def test_paddle_ball_collision(self):
        """Test paddle-ball collision and deflection"""
        # Position ball to hit left paddle
        self.ball.x = self.left_paddle.rect.x + PADDLE_WIDTH
        self.ball.y = self.left_paddle.rect.centery
        self.ball.dx = -INITIAL_BALL_SPEED  # Moving towards the left paddle
        self.assertTrue(self.ball.handle_paddle_collision(self.left_paddle))

        # Position ball to hit right paddle
        self.ball.x = self.right_paddle.rect.x
        self.ball.y = self.right_paddle.rect.centery
        self.ball.dx = INITIAL_BALL_SPEED  # Moving towards the right paddle
        self.assertTrue(self.ball.handle_paddle_collision(self.right_paddle))

    def test_scoring(self):
        """Test scoring system and game state updates"""
        initial_left_score = self.game_state.left_score
        self.game_state.update_score(True)
        self.assertEqual(self.game_state.left_score, initial_left_score + 1)

    def test_game_state(self):
        """Test game state management"""
        # Test score updates
        self.game_state.update_score(True)  # Left player scores
        self.assertEqual(self.game_state.left_score, 1)
        self.assertEqual(self.game_state.right_score, 0)
        self.assertFalse(self.game_state.game_over)

        self.game_state.update_score(False)  # Right player scores
        self.assertEqual(self.game_state.left_score, 1)
        self.assertEqual(self.game_state.right_score, 1)
        self.assertFalse(self.game_state.game_over)

        # Test game over condition
        for _ in range(WINNING_SCORE - 2):  # -2 because we already scored one point
            self.game_state.update_score(True)
            self.assertFalse(self.game_state.game_over)

        self.game_state.update_score(True)  # Left player wins
        self.assertTrue(self.game_state.game_over)
        self.assertEqual(self.game_state.winner, "Left Player")

        # Test reset
        self.game_state.reset()
        self.assertEqual(self.game_state.left_score, 0)
        self.assertEqual(self.game_state.right_score, 0)
        self.assertFalse(self.game_state.game_over)
        self.assertIsNone(self.game_state.winner)

    def test_ball_reset(self):
        """Test ball reset functionality"""
        # Move ball away from center
        self.ball.x = 100
        self.ball.y = 100
        self.ball.speed = 10
        self.ball.dx = 5
        self.ball.dy = 5

        # Reset ball
        self.ball.reset()

        # Check reset properties
        self.assertEqual(self.ball.x, WIDTH // 2)
        self.assertEqual(self.ball.y, HEIGHT // 2)
        self.assertEqual(self.ball.speed, INITIAL_BALL_SPEED)
        self.assertTrue(abs(self.ball.dx) == INITIAL_BALL_SPEED)
        self.assertTrue(abs(self.ball.dy) == INITIAL_BALL_SPEED)


if __name__ == '__main__':
    unittest.main() 