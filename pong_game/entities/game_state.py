from pong_game.utils.constants import WINNING_SCORE


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
