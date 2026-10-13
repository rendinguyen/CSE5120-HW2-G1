"""HW2 search entry points. Use only the documented state methods and turn_O."""
from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool,
            alpha=float('-inf'), beta=float('inf')):
    """TODO M1: alpha-beta minimax; return (O-perspective value, best_move).

    One depth unit is ONE move. At depth zero or a terminal state, return
    (get_scores(terminal), None). O maximizes and X minimizes. The caller's
    maximizingPlayer matches turn_O. Process get_moves() in its given order,
    generate children lazily, keep the FIRST tied move, prune on alpha >= beta.
    Inputs are valid, depth >= 0, alpha < beta. Never mutate a supplied state.
    """
    raise NotImplementedError("Complete minimax")


def negamax(game_status: GameStatus, depth: int, turn_multiplier: int,
            alpha=float('-inf'), beta=float('inf')):
    """TODO N1: alpha-beta negamax; return (current-player value, best_move).

    turn_multiplier is +1 for O, -1 for X and matches the state. At a leaf,
    apply it to get_negamax_scores(terminal). Negate the child's returned value
    and reverse/negate bounds (-beta, -alpha). Same depth/order/tie rules as
    minimax. Implement negamax itself, not a call through to minimax.
    """
    raise NotImplementedError("Complete negamax")
