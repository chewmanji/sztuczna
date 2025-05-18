import copy
from enum import Enum

ROWS_NUMBER = 3
COLS_NUMBER = 2

# Directions (up, down, left, right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Diagonals (top-left, top-right, bottom-left, bottom-right)
DIAGONALS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


class Player(Enum):
    WHITE = 0  # Player 1
    BLACK = 1  # Player 2
    EMPTY = 2


class Clobber:
    def __init__(self, rows: int, cols: int):
        if rows % 2 == 1 and cols % 2 == 1:
            raise Exception(
                "At least one of number of rows or columns must be even number!"
            )
        self.rows = rows
        self.cols = cols
        self.board = self.generate_board(rows, cols)
        self.current_player: Player = Player.BLACK

    def generate_board(self, rows: int, cols: int):
        return [
            [Player.BLACK if (i + j) % 2 == 0 else Player.WHITE for j in range(cols)]
            for i in range(rows)
        ]

    def get_opponent(self, player: Player):
        return Player.BLACK if player == Player.WHITE else Player.WHITE

    def print_board(self):
        print("  " + " ".join(str(j) for j in range(len(self.board[0]))))

        for i, row in enumerate(self.board):
            row_display = []
            for tile in row:
                if tile == Player.WHITE:
                    row_display.append("W")
                elif tile == Player.BLACK:
                    row_display.append("B")
                else:
                    row_display.append("_")

            print(f"{i} {' '.join(row_display)}")

    def get_moves(
        self, player: Player
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        opponent = self.get_opponent(player)
        moves: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == player:
                    for row_dir, col_dir in DIRECTIONS:
                        next_row, next_col = row + row_dir, col + col_dir
                        if 0 <= next_row < self.rows and 0 <= next_col < self.cols:
                            if self.board[next_row][next_col] == opponent:
                                moves.append(((row, col), (next_row, next_col)))
        return moves

    def apply_move(self, move: tuple[tuple[int, int], tuple[int, int]]):
        new_board = copy.deepcopy(self.board)
        (source_row, source_col), (target_row, target_col) = move
        new_board[target_row][target_col] = self.board[source_row][source_col]
        new_board[source_row][source_col] = Player.EMPTY

        self.board = new_board
        self.current_player = self.get_opponent(self.current_player)
