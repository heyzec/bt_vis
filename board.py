from __future__ import annotations
import copy
from typing import Optional

class Board:
    """Captures the objective state of board"""
    def __init__(self, board):
        assert isinstance(board, list)
        self.board = board

    @classmethod
    def generate_init_board(cls):
        board = [
            ['B'] * 6, ['B'] * 6, # 2 black rows
            ['_'] * 6, ['_'] * 6, # 2 empty rows
            ['W'] * 6, ['W'] * 6, # 2 white rows
        ]
        return Board(board)

    def invert(self) -> Board:
        new_board = copy.deepcopy(self.board)
        new_board.reverse()
        for i in range(6):
            for j in range(6):
                if new_board[i][j] == 'W':
                    new_board[i][j] = 'B'
                elif new_board[i][j] == 'B':
                    new_board[i][j] = 'W'
        return Board(new_board)
        
    def is_legal_move(self, src, dst):
        # Not implemented yet
        return True
    
    def move(self, src, dst) -> Optional[Board]:
        """Attempts to move/capture a piece at location. Returns None if move is illegal."""
        i, j = src
        if self.board[i][j] == '_':
            return None
        if not self.is_legal_move(src, dst):
            return None
        
        new_i, new_j = dst
        new_board = copy.deepcopy(self.board)
        piece = new_board[i][j]
        new_board[i][j] = '_'
        new_board[new_i][new_j] = piece
        return Board(new_board)

    
    def game_over(self) -> bool:
        return 'W' in self.board[0] or 'B' in self.board[5]
        
    
    def __repr__(self):
        return f"Board({self.board}"
    
    def print_board(self):
        horizontal_rule = '+' + ('-'*5 + '+') * 6
        for i in range(6):
            print(horizontal_rule)
            print('|  ' +  '  |  '.join(
                ' ' if self.board[i][j] == '_' else self.board[i][j] for j in range(6))
                + '  |')
        print(horizontal_rule)
