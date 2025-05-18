import time
from heruistics import (
    moveable_piece_count,
    isolated_pieces_count,
    blocks_analysis,
)
from clobber import Clobber, Player
from minimax import minimax
from alpha_beta import alpha_beta
from utils import print_stats


# Human vs Agent
def play(algorithm, depth: int, heuristic):
    game = Clobber(2, 3)

    while True:
        valid_moves = game.get_moves(game.current_player)
        if not valid_moves:
            print(f"No valid moves for {game.current_player.name}")
            break

        print(f"Player {game.current_player.name}'s turn")
        game.print_board()
        print(f"Valid moves: {valid_moves}")

        if game.current_player == Player.WHITE:
            start_time = time.time()
            best_eval, best_move, visited_nodes = algorithm(
                game, depth, heuristic, False
            )
            end_time = time.time()
            game.apply_move(best_move)
            print("Visited nodes: " + str(visited_nodes))
            print("Best evaluation:  " + str(best_eval))
            print("Time: ", end_time - start_time)
            print()

        else:
            is_valid = False
            while not is_valid:
                source_row, source_col = map(
                    int, input("Enter source row and column: ").split()
                )
                target_row, target_col = map(
                    int, input("Enter target row and column: ").split()
                )
                move = ((source_row, source_col), (target_row, target_col))

                if move in valid_moves:
                    game.apply_move(move)
                    is_valid = True
                else:
                    print("Invalid move")

    game.print_board()
    winner = game.get_opponent(game.current_player)

    print(f"Player {winner.name} wins!")


# Agent vs Agent
def play_agents(
    algorithm,
    depth: int,
    heuristic_for_white,
    heuristic_for_black,
):
    game = Clobber(5, 6)
    visited_nodes_by_white = 0
    visited_nodes_by_black = 0
    time_white = 0
    time_black = 0

    while True:
        valid_moves = game.get_moves(game.current_player)
        if not valid_moves:
            print(f"No valid moves for {game.current_player.name}")
            break

        elif game.current_player == Player.WHITE:
            start_time = time.time()
            best_eval, best_move, visited_nodes = algorithm(
                game, depth, heuristic_for_white, True
            )
            end_time = time.time()
            visited_nodes_by_white += visited_nodes
            time_white += end_time - start_time
            # print(f"Best evaluation for {game.current_player.name}:  {best_eval}")
            # print()
            game.apply_move(best_move)

        else:
            start_time = time.time()
            best_eval, best_move, visited_nodes = algorithm(
                game, depth, heuristic_for_black, False
            )
            end_time = time.time()
            visited_nodes_by_black += visited_nodes
            time_black += end_time - start_time
            # print(f"Best evaluation for {game.current_player.name}:  {best_eval}")
            # print()
            game.apply_move(best_move)

    game.print_board()
    winner = game.get_opponent(game.current_player)

    print(f"Player {winner.name} wins!\n")
    print_stats(visited_nodes_by_white, visited_nodes_by_black, time_white, time_black)
    return (
        winner,
        visited_nodes_by_white,
        visited_nodes_by_black,
        time_white,
        time_black,
    )


if __name__ == "__main__":
    # play_agents(minimax, 2, isolated_pieces_count, evaluate_connectivity)
    # play_agents(alpha_beta, 3, isolated_pieces_count, evaluate_connectivity)
    play_agents(minimax, 3, isolated_pieces_count, blocks_analysis)
