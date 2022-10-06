import pygame
import asyncio
from pypipe.pipe import Pipe
from py_scm.director import Director
from bt_vis.game_scene import GameScene

pipe = Pipe('/tmp/board', 'o')
pipe_action1 = Pipe('/tmp/action1', 'o')
pipe_action2 = Pipe('/tmp/action2', 'o')

pygame.init()

pygame.display.set_caption('Quick Start')


WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400


from bt_vis.constants import BOARD_UPDATED



director = Director()
my_scene = GameScene()
director.set_scene(my_scene)

async def listener():
    while True:
        try:
            board = await pipe_action1.read_async()
            if board is not None:
                director.event_from_outside(pygame.event.Event(BOARD_UPDATED, board=board))
        except EOFError:
            print("oops")
        await asyncio.sleep(0.5)

def main():
    try:
        loop = asyncio.new_event_loop()
        loop.create_task(listener())
        loop.run_until_complete(director.loop())
    except Exception as err:
        import traceback
        traceback.print_exc()
    finally:
        child_proc.terminate()
