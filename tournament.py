from bt_ai.game import PlayerAI
import utils

from pypipe.pipe import Pipe

pipe = Pipe('/tmp/board', 'o')
pipe_action1 = Pipe('/tmp/action1', 'o')
pipe_action2 = Pipe('/tmp/action2', 'o')

class PlayerManual:
    def make_move(self, board):
        pipe_action1.write(board)
        data = pipe_action2.read_sync()
        if len(data) != 2:
            print("OH NO")
            return
        return data


class Tournament:
    def __init__(self, player1, player2):
        self.move = 0
        self.board = Tournament.generate_init_board()
        self.player1 = player1
        self.player2 = player2
        
    def game_over(self):
        return ('B' in self.board[5] or 'W' in self.board[0])


    def is_black_turn(self):
        return self.move % 2 == 0

    @staticmethod
    def generate_init_board():
        board = [
            ['B'] * 6, ['B'] * 6, # 2 black rows
            ['_'] * 6, ['_'] * 6, # 2 empty rows
            ['W'] * 6, ['W'] * 6, # 2 white rows
        ]
        return board
    

    def play(self):
        while not self.game_over():
            if self.is_black_turn():
                player = self.player1
            else:
                player = self.player2
            
            if not self.is_black_turn():
                utils.invert_board(self.board)
            move = player.make_move(self.board)
            src, dst = move
            utils.state_change(self.board, src, dst) # makes the move effective on the board
            if not self.is_black_turn():
                utils.invert_board(self.board)

            colour = "someone"
            print(f'Move No: {move} by {colour}')
            utils.print_state(self.board) # printing the current configuration of the board after making move
            pipe_action1.write(self.board)
            self.move += 1
            
        
def main():
    tournament = Tournament(PlayerManual(), PlayerAI())
    tournament.play()
    
main()
        
