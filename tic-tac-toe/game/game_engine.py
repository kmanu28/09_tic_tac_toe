"""
GameEngine: owns the board, turns, round results,
scoreboard, and first-player selection.
"""

import pygame

from game.ai import choose_move
from game.renderer import board_pos_to_cell
from game.rules import check_winner, is_board_full

HUMAN_SYMBOL = "X"
COMPUTER_SYMBOL = "O"


class GameEngine:
    def __init__(self):
        self.scores = {
            "X": 0,
            "O": 0,
            "draws": 0,
        }

        self.starting_player = HUMAN_SYMBOL
        self.reset_round()

    def reset_round(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = self.starting_player
        self.round_over = False
        self.winner = None

        if self.current_player == COMPUTER_SYMBOL:
            self._maybe_take_computer_turn()

    def reset_match(self):
        self.scores = {
            "X": 0,
            "O": 0,
            "draws": 0,
        }

        # Keep the selected starter when resetting the match.
        self.reset_round()

    def handle_click(self, pos):
        if self.round_over:
            return

        if self.current_player != HUMAN_SYMBOL:
            return

        cell = board_pos_to_cell(pos)

        if cell is None:
            return

        row, col = cell

        # Occupied cells must not change the board or the turn.
        if self.board[row][col] is not None:
            return

        self.board[row][col] = HUMAN_SYMBOL
        self.check_round_end()

        if self.round_over:
            return

        self.current_player = COMPUTER_SYMBOL
        self._maybe_take_computer_turn()

    def _maybe_take_computer_turn(self):
        if self.round_over:
            return

        if self.current_player != COMPUTER_SYMBOL:
            return

        move = choose_move(self.board)

        if move is None:
            return

        row, col = move

        if self.board[row][col] is not None:
            return

        self.board[row][col] = COMPUTER_SYMBOL
        self.check_round_end()

        if self.round_over:
            return

        self.current_player = HUMAN_SYMBOL

    def handle_keydown(self, key):
        if key == pygame.K_x:
            # X starts the next round.
            self.starting_player = HUMAN_SYMBOL

        elif key == pygame.K_o:
            # O starts the next round.
            self.starting_player = COMPUTER_SYMBOL

        elif key == pygame.K_r:
            # Restart the current round and preserve the scoreboard.
            self.reset_round()

        elif key == pygame.K_m:
            # Reset the scoreboard and start a new round.
            self.reset_match()

    def check_round_end(self):
        if self.round_over:
            return

        winner = check_winner(self.board)

        # Always check for a winner before checking for a draw.
        if winner is not None:
            self.round_over = True
            self.winner = winner
            self.scores[winner] += 1
            return

        if is_board_full(self.board):
            self.round_over = True
            self.winner = None
            self.scores["draws"] += 1

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_board(surface, self.board)

        if self.round_over:
            turn_text = "Round over"
        elif self.current_player == HUMAN_SYMBOL:
            turn_text = "Your turn (X)"
        else:
            turn_text = "Computer's turn (O)"

        renderer.draw_text(surface, font, turn_text, (16, 18))

        scoreboard_text = (
            f"X: {self.scores['X']}    "
            f"O: {self.scores['O']}    "
            f"Draws: {self.scores['draws']}"
        )

        renderer.draw_text(surface, font, scoreboard_text, (16, 58))

        if self.round_over:
            result_text = f"{self.winner} wins!" if self.winner else "Draw!"
            renderer.draw_result(surface, font, result_text)

        renderer.draw_controls(
            surface,
            font,
            f"Next starter: {self.starting_player}",
        )