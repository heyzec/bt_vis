import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from pypipe.pipe import Pipe
from py_scm.handler import Handler
from py_scm.node import Node

BLOCK_SIZE = 50
from bt_vis.constants import BLACK, BOARD_REFRESH, PIPE_FILE_SEND_USER_ACTION, WHITE
from bt_vis import utils


class Board(Node):
    pipe = Pipe(PIPE_FILE_SEND_USER_ACTION, 'o')

    def __init__(self):
        super().__init__()
        self.selected = None
        self.board = None
        self.attach(Handler(self.on_click, pygame.MOUSEBUTTONDOWN))
        self.attach(Handler(self.on_board_update, BOARD_REFRESH))

    def on_click(self, event, context):
        new_selection = Board.click_to_coord(event, self.x, self.y)
        if new_selection == self.selected:
            self.selected = None
            return

        if self.selected is not None:
            self.pipe.write([self.selected, new_selection])
            self.selected = None
            return

        self.selected = new_selection
    
    def on_board_update(self, event, context):
        if event is None:
            # Weird
            return
        if event.board is not None:
            self.board = event.board

    def draw(self, surface):
        if self.board is None:
            return
        self.draw_board(surface)
        if self.selected is not None:
            pass
    
    @property
    def width(self):
        return 6 * BLOCK_SIZE

    @property
    def height(self):
        return 6 * BLOCK_SIZE
        
    def draw_board(self, surface):
        x_offset, y_offset = self.x, self.y
        for i in range(6):
            for j in range(6):
                self.draw_grid(surface, self.board[i][j], i, j)

        if self.selected is None:
            return
        sel_i, sel_j = self.selected
        rect = pygame.Rect(sel_j * BLOCK_SIZE + x_offset, sel_i * BLOCK_SIZE + y_offset, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, (100, 200, 0, 150), rect, 2)

    def draw_grid(self, surface, piece, i, j, color=BLACK):
        x_offset, y_offset = self.x, self.y
        rect = pygame.Rect(j * BLOCK_SIZE + x_offset, i * BLOCK_SIZE + y_offset, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, BLACK, rect, 2)

        centre_x, centre_y = (j + 0.5) * BLOCK_SIZE, (i + 0.5) * BLOCK_SIZE
        colour = None
        if piece == 'W':
            colour = WHITE
        elif piece == 'B':
            colour = BLACK
        if colour is not None:
            pygame.draw.circle(surface, colour, (centre_x + x_offset, centre_y + y_offset), 10)

    @staticmethod
    def click_to_coord(event, x_start, y_start):
        x, y = event.pos
        i = (x - x_start) / BLOCK_SIZE
        j = (y - y_start) / BLOCK_SIZE
        assert (0 <= i < 6 and 0 <= j < 6)
        return [int(j), int(i)]


