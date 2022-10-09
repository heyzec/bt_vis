"""Deals with board moves, validity, restarts, players"""
import asyncio
import subprocess

import utils
from pypipe.pipe import Pipe
from bt_vis.constants import PIPE_FILE_BOARD_UPDATES

pipe_board_updates = Pipe(PIPE_FILE_BOARD_UPDATES, 'o')

class GameNode:
    def __init__(self, board):
        self.parent = None
        self.children = []
        self.board = board
    
    def add_child(self, node):
        self.children.append(node)
        node.parent = self


class Driver:
    def __init__(self):
        self.board = None
        self.selected = None
        self.root_node = GameNode(utils.generate_init_state())
        self.head_node = self.root_node
        self.child_proc = None


    def start_helper(self):
        self.child_proc = subprocess.Popen(["python","helper.py"])

    async def listener(self):
        while True:
            try:
                board = await pipe_board_updates.read_async()
            except EOFError:
                print("oops")
                continue
            if board is None:
                continue
            if board == self.head_node.board:
                continue
            self.board = board
            new_node = GameNode(board)
            self.head_node.add_child(new_node)
            self.head_node = new_node

            await asyncio.sleep(0.5)
            

            
    def set_director(self, director):
        self.director = director

    def undo(self):
        if self.head_node.parent is None:
            return
        self.head_node = self.head_node.parent

    def redo(self):
        if len(self.head_node.children) == 0:
            return
        self.head_node = self.head_node.children[0]

    async def run(self):
        await self.listener()

    def kill_child_proc(self):
        if self.child_proc is not None:
            self.child_proc.terminate()
