"""Deals with board moves, validity, restarts, players"""
from __future__ import annotations
import asyncio
from multiprocessing import Process

from typing import Optional
from bt_ai.player_ai import PlayerAI
from bt_vis.player import PlayerManual
from bt_vis.tournament import Tournament
from py_scm.director import Director

import utils
from pypipe.pipe import Pipe
from bt_vis.constants import PIPE_FILE_BOARD_UPDATES, PIPE_FILE_SEND_USER_ACTION

pipe_board_updates = Pipe(PIPE_FILE_BOARD_UPDATES, 'o')
pipe_send_user_action = Pipe(PIPE_FILE_SEND_USER_ACTION, 'o')

class GameNode:
    """Stores the raw state of the board and its history."""
    def __init__(self, board: list[list[str]]):
        self.parent: Optional[GameNode] = None
        self.children: list[GameNode] = []
        self.board = board

    def add_child(self, node: GameNode):
        """Create a new node that branches off the current node."""
        self.children.append(node)
        node.parent = self


class Driver:
    """A game engine."""
    def __init__(self):
        self.board = None
        self.selected = None
        self.root_node = GameNode(utils.generate_init_state())
        self.head_node = self.root_node
        self.child_proc = None
        self.director = None


    def start_helper(self):
        def f():
            tournament = Tournament(PlayerAI(), PlayerManual())
            tournament.play_until_game_over()
        p = Process(target=f)
        p.start()
        self.child_proc = p

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
            new_node = GameNode(board)  # type: ignore
            self.head_node.add_child(new_node)
            self.head_node = new_node

            await asyncio.sleep(0.01)
    
    def send_action(self, action):
        pipe_send_user_action.write(action)

    def set_director(self, director: Director):
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
        """Starts the game engine."""
        await self.listener()

    def kill_child_proc(self):
        """Terminates the child process."""
        if self.child_proc is not None:
            self.child_proc.terminate()
