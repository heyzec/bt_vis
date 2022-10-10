"""Players that takes part in a tournament."""
import abc

from bt_vis.constants import PIPE_FILE_SEND_USER_ACTION
from pypipe.pipe import Pipe

pipe_send_user_action = Pipe(PIPE_FILE_SEND_USER_ACTION, 'o')

class Player(abc.ABC):
    """An abstract superclass player who takes part in a tournament."""
    @abc.abstractmethod
    def make_move(self, board) -> list[list[int]]:
        """Returns a raw action move that the player intends to make."""
        raise NotImplementedError()

    @abc.abstractmethod
    def make_move_with_eval(self, board) -> tuple[list[list[int]], float]:
        """Returns a raw action move, as well as the player's evaluation score of move."""
        raise NotImplementedError()

class PlayerManual(Player):
    """Player that makes moves based on inputs via the visualiser."""
    def make_move(self, board) -> list[list[int]]:
        data = pipe_send_user_action.read_sync()
        assert isinstance(data, list)
        if len(data) != 2:
            raise Exception("Received a non-action")
        return data

    def make_move_with_eval(self, board) -> tuple[list[list[int]], float]:
        return self.make_move(board), 0
