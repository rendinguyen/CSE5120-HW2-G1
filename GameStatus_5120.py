"""HW2 scored tic-tac-toe. No graphics or third-party dependencies."""


class GameStatus:
    def __init__(self, board_state, turn_O=True):
        """Provided: copy a square board (size 3 through 8) into immutable rows.

        +1 is O, -1 is X, 0 is empty. turn_O indicates the next player.
        Do not impose mark-count parity: tests include constructed positions.
        """
        board = tuple(tuple(row) for row in board_state)
        if not 3 <= len(board) <= 8 or any(len(row) != len(board) for row in board):
            raise ValueError("board must be square with size 3 through 8")
        if any(type(v) is not int or v not in (-1, 0, 1) for row in board for v in row):
            raise ValueError("cells must be integer -1, 0 or 1")
        if type(turn_O) is not bool:
            raise ValueError("turn_O must be bool")
        self.board_state = board
        self.turn_O = turn_O

    def windows(self):
        """Provided: yield each length-three window once, including overlaps."""
        n = len(self.board_state)
        for r in range(n):
            for c in range(n):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    if 0 <= r + 2 * dr < n and 0 <= c + 2 * dc < n:
                        yield tuple(self.board_state[r + i * dr][c + i * dc] for i in range(3))

    def is_terminal(self):
        """TODO S1: bool, true iff no empty cell remains. A triplet does not end play."""
        raise NotImplementedError("Complete is_terminal")

    def get_moves(self):
        """TODO S2: list of empty (row, col) tuples in row-major order."""
        raise NotImplementedError("Complete get_moves")

    def get_new_state(self, move):
        """TODO S3: new GameStatus with one mark and flipped turn; preserve this state.

        Reject malformed, outside-board, or occupied moves with ValueError.
        Accept a length-two tuple/list of non-bool integers.
        """
        raise NotImplementedError("Complete get_new_state")

    def triplet_counts(self):
        """TODO S4: (O_count, X_count), counting overlapping completed triplets."""
        raise NotImplementedError("Complete triplet_counts")

    def get_scores(self, terminal):
        """TODO S5: fixed O-perspective evaluation, never human-relative.

        terminal=True: 100 * (O completed triplets - X completed triplets).
        terminal=False: for EACH length-three window, add +100/+10/+1 for
        3/2/1 O marks and no X marks; subtract the same for X and no O.
        Empty or mixed windows contribute zero. No randomness or custom weights.
        """
        raise NotImplementedError("Complete get_scores")

    def get_negamax_scores(self, terminal):
        """Provided: same O-perspective evaluation; negamax applies the sign."""
        return self.get_scores(terminal)
