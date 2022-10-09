import abc

from bt_vis.constants import PIPE_FILE_SEND_USER_ACTION
from pypipe.pipe import Pipe

pipe_send_user_action = Pipe(PIPE_FILE_SEND_USER_ACTION, 'o')

class Player(abc.ABC):
    @abc.abstractmethod
    def make_move(self, board):
        raise NotImplementedError()

class PlayerManual(Player):
    def make_move(self, board):
        data = pipe_send_user_action.read_sync()
        if len(data) != 2:
            print("OH NO")
            return
        return data
