import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import pyperclip
import pygame
from bt_vis.driver import Driver
from bt_vis.grid import Grid
from py_scm.button import Button
from py_scm.col import Col
from py_scm.handler import Handler
from py_scm.row import Row

from py_scm.scene import Scene

BLOCK_SIZE = 50
BLACK = pygame.Color('#000000')
WHITE = pygame.Color('#FFFFFF')
BEIGE = pygame.Color('#f0bc7a')

from bt_vis.constants import BOARD_REFRESH, USER_SELECTED

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.driver = None
    
    def set_driver(self, driver: Driver):
        self.driver = driver

    @property
    def height(self):
        return 600

    @property
    def width(self):
        return 598
    
    def get_board(self):
        assert self.driver is not None
        return self.driver.head_node.board

    def on_draw(self, screen):
        screen.fill(BEIGE)
        self.refresh_board(self.get_board())
        super().on_draw(screen)
        
    def refresh_board(self, board):
        self.handle(pygame.event.Event(BOARD_REFRESH, board=board, driver=self.driver), None)
        
    def on_back(self, event, context):
        assert self.driver is not None
        self.driver.undo()
        self.refresh_board(self.get_board())

    def on_next(self, event, context):
        assert self.driver is not None
        self.driver.redo()
        self.refresh_board(self.get_board())
        
    def on_restart(self, event, context):
        assert self.driver is not None
        self.driver.start_helper()
        
    def on_copy(self, event, context):
        pyperclip.copy(repr(self.get_board()))
        
    def on_user_input(self, event, context):
        assert self.driver is not None
        self.driver.send_action(event.action)

    
    def on_setup(self):
        assert self.driver is not None
        self.driver.start_helper()

        self.attach(Handler(self.on_user_input, USER_SELECTED))

        board = Grid()
        self.board = board
        
        btn_back = Button("Back")
        btn_back.attach(Handler(self.on_back, pygame.MOUSEBUTTONDOWN))
        btn_next = Button("Next")
        btn_next.attach(Handler(self.on_next, pygame.MOUSEBUTTONDOWN))
        btn_restart = Button("Restart")
        btn_restart.attach(Handler(self.on_restart, pygame.MOUSEBUTTONDOWN))
        btn_copy = Button("Copy Board")
        btn_copy.attach(Handler(self.on_copy, pygame.MOUSEBUTTONDOWN))
        
        row = Row()
        row.add(btn_back, btn_next, btn_restart, btn_copy)
        
        col = Col()
        col.add(board, row)

        self.place(col, 200, 40)
        self.refresh_board(self.get_board())
