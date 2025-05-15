import copy
from clobber import Clobber, Player
from collections.abc import Callable


# Implementation of alpha-beta pruning
def alpha_beta(
    game: Clobber,
    depth: int,
    heuristic: Callable[[Clobber, Player], int],
    maximizing_player: bool,
    alpha=float("-inf"),
    beta=float("inf"),
    visited_nodes=0,
):
    visited_nodes += 1

    possible_moves = game.get_moves(game.current_player)

    if depth == 0 or len(possible_moves) == 0:
        return heuristic(game, game.current_player), None, visited_nodes

    if maximizing_player:
        max_eval = float("-inf")
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.apply_move(move)
            eval, _, nodes = alpha_beta(
                game_copy, depth - 1, heuristic, False, alpha, beta, 0
            )
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
            visited_nodes += nodes
        return max_eval, best_move, visited_nodes

    else:
        min_eval = float("inf")
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.apply_move(move)
            eval, _, nodes = alpha_beta(
                game_copy, depth - 1, heuristic, True, alpha, beta, 0
            )
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
            visited_nodes += nodes
        return min_eval, best_move, visited_nodes
