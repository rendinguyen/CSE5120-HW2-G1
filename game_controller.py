"""Headless controller used by the supplied renderer and the autograder."""
from GameStatus_5120 import GameStatus
import multiAgents


class GameController:
    def __init__(self, size=4, human_symbol='O', algorithm='minimax', depth=2):
        """Provided: settings, then new game. The HUMAN always moves first."""
        if type(size) is not int or not 3 <= size <= 8:
            raise ValueError('size must be 3 through 8')
        if human_symbol not in ('O', 'X') or algorithm not in ('minimax', 'negamax'):
            raise ValueError('invalid symbol or algorithm')
        if type(depth) is not int or not 1 <= depth <= 4:
            raise ValueError('controller depth must be 1 through 4')
        self.size, self.human_symbol = size, human_symbol
        self.algorithm, self.depth = algorithm, depth
        self.reset()

    def reset(self):
        """TODO C1: empty board of self.size, human to move, preserve settings."""
        raise NotImplementedError("Complete reset")

    def human_move(self, row, col):
        """TODO C2: apply ONE legal human move; bool accepted. Never call the AI.

        Wrong turn, terminal state, malformed/out-of-range/occupied coordinates:
        return False without changing state. A valid move returns True.
        """
        raise NotImplementedError("Complete human_move")

    def ai_move(self):
        """TODO C3: apply ONE AI move and return its (row,col), or None if inactive.

        On the AI turn call the selected multiAgents function with self.depth
        and the correct bool/sign. Wrong turn or terminal: no search, no change.
        A faulty search returning an illegal/None move on an active turn raises
        ValueError without changing state. Do not silently substitute a move.
        """
        raise NotImplementedError("Complete ai_move")

    def status(self):
        """TODO C4: exact dictionary: terminal, turn, O, X, winner.

        turn is 'O' or 'X' while active, None when terminal. O/X are raw triplet
        counts. winner is None while active, then 'O', 'X', or 'Draw'. Pure query.
        """
        raise NotImplementedError("Complete status")
