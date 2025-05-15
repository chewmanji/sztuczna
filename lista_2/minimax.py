import copy
from clobber import Clobber, Player
from collections.abc import Callable


# Implementation of minimax algorithm
def minimax(
    game: Clobber,
    depth: int,
    heuristic: Callable[[Clobber, Player], int],
    maximizing_player: bool,
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
            eval, _, nodes = minimax(game_copy, depth - 1, heuristic, False, 0)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            visited_nodes += nodes
        return max_eval, best_move, visited_nodes

    else:
        min_eval = float("inf")
        best_move = None
        for move in possible_moves:
            game_copy = copy.deepcopy(game)
            game_copy.apply_move(move)
            eval, _, nodes = minimax(game_copy, depth - 1, heuristic, True, 0)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            visited_nodes += nodes
        return min_eval, best_move, visited_nodes
