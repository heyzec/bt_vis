from typing import Optional
from bt_ai.player_ai import PlayerAI
from bt_vis.board import Board
from bt_vis.player import Player, PlayerManual

from bt_vis.constants import PIPE_FILE_BOARD_UPDATES
from pypipe.pipe import Pipe

pipe_board_updates = Pipe(PIPE_FILE_BOARD_UPDATES, 'o')


class Tournament:
    def __init__(self, black: Player, white: Player, initial_board: Optional[Board] = None,
            show_board=False):
        if initial_board is None:
            initial_board = Board.generate_init_board()
        assert isinstance(initial_board, Board)

        self.move = 0
        self.board = initial_board
        self.black = black
        self.white = white
        self.black_eval = None
        self.white_eval = None
        self.show_board = show_board
        self.winner = None

    def is_black_turn(self):
        return self.move % 2 == 0


    def play_once(self):
        assert not self.board.game_over()
        if self.is_black_turn():
            player = self.black
        else:
            player = self.white

        if not self.is_black_turn():
            self.board = self.board.invert()
        move, val = player.make_move_with_eval(self.board.board)
        src, dst = move
        # makes the move effective on the board
        self.board = self.board.move(src, dst)
        if not self.is_black_turn():
            self.board = self.board.invert()

        colour = "someone"
        print(f'Move No: {move} by {type(player).__name__}')
        if self.show_board:
            # printing the current configuration of the board after making move
            self.board.print_board()
        pipe_board_updates.write(self.board.board)
        self.move += 1

        if self.board.game_over():
            print("GAME OVER")
            self.winner = player
        return move, val

    def play_until_game_over(self):
        while True:
            self.play_once()
            if self.winner is not None:
                break


def main():
    # tournament = Tournament(PlayerManual(), PlayerAI())
    tournament = Tournament(PlayerAI(), PlayerManual())
    # tournament = Tournament(PlayerAI(), PlayerAI())
    tournament.play_until_game_over()

if __name__ == '__main__':
    main()
