from clobber import Clobber, Player, DIRECTIONS, DIAGONALS


# count number of pieces which can move
def moveable_piece_count(game: Clobber, player: Player):
    count = 0
    opponent = game.get_opponent(player)
    for row in range(game.rows):
        for col in range(game.cols):
            if game.board[row][col] == player:
                for row_dir, col_dir in DIRECTIONS:
                    next_row, next_col = row + row_dir, col + col_dir
                    if (
                        0 <= next_row < game.rows
                        and 0 <= next_col < game.cols
                        and game.board[next_row][next_col] == opponent
                    ):
                        count += 1
                        break

    return count if player == Player.WHITE else -count


# makes some sense
def isolated_pieces_count(game: Clobber, player: Player):
    count = 0
    opponent = game.get_opponent(player)
    for row in range(game.rows):
        for col in range(game.cols):
            if game.board[row][col] == player:
                if not any(
                    0 <= row + row_dir < game.rows
                    and 0 <= col + col_dir < game.cols
                    and game.board[row + row_dir][col + col_dir] == opponent
                    for row_dir, col_dir in DIRECTIONS
                ):
                    count += 1

    return count if player == Player.WHITE else -count


# Simplified Rafal's algorithm - https://www.researchgate.net/publication/221932254_New_Trends_in_Clobber_Programming
def blocks_analysis(game: Clobber, player: Player) -> float:
    player_blocks = find_groups(game, player)
    evaluation_score = 0
    for block in player_blocks:
        evaluation_score += analyze_block(block, game, player)

    return evaluation_score if player == Player.WHITE else -evaluation_score


def find_groups(game: Clobber, player: Player) -> list[set[tuple[int, int]]]:
    visited = set()
    groups = []

    def dfs(r, c, group):
        if (r, c) in visited or not (0 <= r < game.rows and 0 <= c < game.cols):
            return

        if game.board[r][c] == Player.EMPTY:
            return

        visited.add((r, c))
        group.add((r, c))

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            dfs(nr, nc, group)

    for r in range(game.rows):
        for c in range(game.cols):
            if game.board[r][c] == player and (r, c) not in visited:
                group = set()
                dfs(r, c, group)
                groups.append(group)

    return groups


def analyze_block(block: set[tuple[int, int]], game: Clobber, player: Player) -> float:
    opponent = game.get_opponent(player)

    # check if block contains only one player's pieces
    contains_enemy_pieces = False
    for row, col in block:
        if game.board[row][col] == opponent:
            contains_enemy_pieces = True
            break

    if not contains_enemy_pieces:
        return 0

    player_score = calculate_block_score(block, game, player, opponent)
    opponent_score = calculate_block_score(block, game, opponent, player)

    return (
        player_score / opponent_score
        if player_score > opponent_score
        else -opponent_score / player_score
    )


def calculate_block_score(
    block: set[tuple[int, int]], game: Clobber, player: Player, opponent: Player
):
    score = 0

    for piece in block:
        orthogonal_count = 0
        diagonal_count = 0
        row, col = piece
        if game.board[row][col] != player:
            continue

        # calculate O(s_c)
        for row_dir, col_dir in DIRECTIONS:
            next_row, next_col = row + row_dir, col + col_dir
            if (
                0 <= next_row < game.rows
                and 0 <= next_col < game.cols
                and game.board[next_row][next_col] == opponent
            ):
                orthogonal_count += 1

        # calculate D(s_c)
        for row_diag, col_diag in DIAGONALS:
            diagonal_row, diagonal_col = row + row_diag, col + col_diag

            # Check if diagonal position is within bounds and contains player's stone
            if (
                0 <= diagonal_row < game.rows
                and 0 <= diagonal_col < game.cols
                and game.board[diagonal_row][diagonal_col] == player
            ):
                is_tied = False

                # Check all orthogonal neighbors of the original stone for opponent stones
                for dr, dc in DIRECTIONS:
                    neighbor_row, neighbor_col = row + dr, col + dc

                    if (
                        0 <= neighbor_row < game.rows
                        and 0 <= neighbor_col < game.cols
                        and game.board[neighbor_row][neighbor_col] == opponent
                    ):
                        # Check if this opponent stone is also adjacent to the diagonal stone
                        if (
                            abs(neighbor_row - diagonal_row) <= 1
                            and abs(neighbor_col - diagonal_col) <= 1
                            and (neighbor_row, neighbor_col)
                            != (diagonal_row, diagonal_col)
                        ):
                            is_tied = True
                            break

                if is_tied:
                    diagonal_count += 1

        score += 1 + orthogonal_count + diagonal_count

    return score
