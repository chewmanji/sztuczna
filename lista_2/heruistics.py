from clobber import Clobber, Player, DIRECTIONS


# doesn't have much sense since it's always the same for both players
def possible_moves_count(game: "Clobber", player: "Player"):
    count = len(game.get_moves(player))
    return count if player == Player.WHITE else -count


# not the best but better than possible_moves_count
def piece_count(game: "Clobber", player: "Player"):
    count = sum(row.count(player) for row in game.board)
    return count if player == Player.WHITE else -count


# makes some sense
def isolated_pieces_count(game: "Clobber", player: "Player"):
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


def evaluate_connectivity(game: Clobber, player: Player) -> float:
    """
    The heuristic considers:
    1. Isolation value - pieces that cannot move are dead
    2. Connectivity to opponent pieces - more connections means more options
    3. Grouped pieces that can support each other
    """

    opponent = game.get_opponent(player)
    # Track mobility and isolation
    mobility = 0
    isolated = 0

    # Track overall connectivity to opponent pieces
    connectivity = 0

    # Group analysis
    groups = find_connected_groups(game, player)

    # Count white piece connectivity
    for r in range(game.rows):
        for c in range(game.cols):
            if game.board[r][c] == player:
                # Check adjacent positions for opponent pieces
                adjacent_enemies = 0
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < game.rows
                        and 0 <= nc < game.cols
                        and game.board[nr][nc] == opponent
                    ):
                        adjacent_enemies += 1
                        connectivity += 1

                # Mobility and isolation tracking
                if adjacent_enemies > 0:
                    mobility += adjacent_enemies
                else:
                    isolated += 1

    # Calculate group control scores
    # Groups with many connections to opponent pieces are valuable
    group_score = analyze_groups(groups, game, opponent)

    # Weight the different components of the evaluation
    isolation_weight = 2.0
    mobility_weight = 1.0
    connectivity_weight = 1.5
    group_weight = 2.5

    # Calculate the final score
    score = (
        mobility_weight * mobility
        - isolation_weight * isolated
        + connectivity_weight * connectivity
        + group_weight * group_score
    )

    return score if player == Player.WHITE else -score


def find_connected_groups(game: Clobber, player: Player) -> list[set[tuple[int, int]]]:
    """Find all connected groups of pieces for the given player"""
    visited = set()
    groups = []

    def dfs(r, c, group):
        """Depth-first search to find all connected pieces"""
        if (r, c) in visited or not (0 <= r < game.rows and 0 <= c < game.cols):
            return

        if game.board[r][c] != player:
            return

        visited.add((r, c))
        group.add((r, c))

        for dr, dc in DIRECTIONS:
            dfs(r + dr, c + dc, group)

    # Find all connected groups using DFS
    for r in range(game.rows):
        for c in range(game.cols):
            if game.board[r][c] == player and (r, c) not in visited:
                group = set()
                dfs(r, c, group)
                groups.append(group)

    return groups


def analyze_groups(
    groups: list[set[tuple[int, int]]], game: Clobber, opponent: Player
) -> float:
    """
    Analyze groups for strategic value
    Returns a score based on the groups' characteristics
    """
    total_score = 0

    for group in groups:
        group_size = len(group)
        interactable_pieces = 0  # Pieces that can interact with opponents

        # Calculate border pieces (pieces that can interact with opponents)
        for r, c in group:
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < game.rows
                    and 0 <= nc < game.cols
                    and game.board[nr][nc] == opponent
                ):
                    interactable_pieces += 1
                    break

        # Calculate group value
        # Groups with more interactable pieces relative to their size are more valuable
        if group_size > 0:
            interactable_ratio = interactable_pieces / group_size
            # Value groups that have high interactable_ratio (can interact with opponents)
            # but also give some value to larger groups
            group_score = group_size * (0.5 + interactable_ratio)
            total_score += group_score

    return total_score
