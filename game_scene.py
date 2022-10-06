import subprocess
import pyperclip
import pygame
from bt_vis.board import Board
from py_scm.button import Button
from py_scm.col import Col
from py_scm.handler import Handler
from py_scm.row import Row

from py_scm.scene import Scene
import utils

BLOCK_SIZE = 50
BLACK = pygame.Color('#000000')
WHITE = pygame.Color('#FFFFFF')
BEIGE = pygame.Color('#f0bc7a')

from bt_vis.constants import BOARD_REFRESH, BOARD_UPDATED

class GameNode:
    def __init__(self, board):
        self.parent = None
        self.children = []
        self.board = board
    
    def add_child(self, node):
        self.children.append(node)
        node.parent = self

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.board = None
        self.selected = None
        self.root_node = GameNode(utils.generate_init_state())
        self.head_node = self.root_node

    @property
    def height(self):
        return 600

    @property
    def width(self):
        return 598

    def on_draw(self, screen):
        screen.fill(BEIGE)
        super().on_draw(screen)
        
    def on_event(self, event, context):
        super().on_event(event, context)
        if event.type == BOARD_UPDATED:
            new_board = event.board
            if new_board == self.head_node.board:
                return
            self.board = new_board
            new_node = GameNode(new_board)
            self.head_node.add_child(new_node)
            self.head_node = new_node
            self.refresh_board(new_board)
        
    def refresh_board(self, board):
        self.handle(pygame.event.Event(BOARD_REFRESH, board=board), None)
        
    def on_back(self, event, context):
        if self.head_node.parent is None:
            return
        self.head_node = self.head_node.parent
        self.refresh_board(self.head_node.board)

    def on_next(self, event, context):
        if len(self.head_node.children) == 0:
            return
        self.head_node = self.head_node.children[0]
        self.refresh_board(self.head_node.board)
        
    def on_restart(self, event, context):
        child_proc = subprocess.Popen(["python","helper.py"])
        
    def on_copy(self, event, context):
        pyperclip.copy(repr(self.head_node.board))

    
    def on_setup(self):
        child_proc = subprocess.Popen(["python","helper.py"])
        board = Board()
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

        self.refresh_board(self.head_node.board)
