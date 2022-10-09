import random
from bt_ai.player_ai import PlayerAI
from bt_vis.board import Board
from bt_vis.player import Player, PlayerManual
import utils

from bt_vis.constants import PIPE_FILE_BOARD_UPDATES
from pypipe.pipe import Pipe

pipe_board_updates = Pipe(PIPE_FILE_BOARD_UPDATES, 'o')


class Tournament:
    def __init__(self, player1: Player, player2: Player, initial_board=None, show_board=False):
        if initial_board is None:
            initial_board = Board.generate_init_board()

        self.move = 0
        self.board: Board = initial_board
        self.player1 = player1
        self.player2 = player2
        self.show_board = show_board
        
    def is_black_turn(self):
        return self.move % 2 == 0
    

    def play(self):
        while not self.board.game_over():
            if self.is_black_turn():
                player = self.player1
            else:
                player = self.player2
            
            if not self.is_black_turn():
                self.board = self.board.invert()
            move = player.make_move(self.board.board)
            src, dst = move
            # makes the move effective on the board
            self.board = self.board.move(src, dst)
            if not self.is_black_turn():
                self.board = self.board.invert()

            colour = "someone"
            print(f'Move No: {move} by {type(player).__name__}')
            if self.show_board:
                # printing the current configuration of the board after making move
                utils.print_state(self.board)
            pipe_board_updates.write(self.board.board)
            self.move += 1
            
        
def main():
    # tournament = Tournament(PlayerManual(), PlayerAI())
    tournament = Tournament(PlayerAI(), PlayerManual())
    tournament = Tournament(PlayerAI(), PlayerAI())
    tournament.play()
    
if __name__ == '__main__':
    main()
        
