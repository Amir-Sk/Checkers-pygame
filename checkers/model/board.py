import pygame
from services.constants import ROWS, COLS, BLACK, GREY, WHITE, SQUARE_SIZE, WOOD
from model.piece import Piece


class Board:

    def __init__(self):
        self.board = []
        self.remaining_w = self.remaining_b = 12
        self.create_board()

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw_squares(self, win):
        win.fill(WOOD)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(
                    win,
                    GREY,
                    (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                )

    def remove(self, pieces):
        for p in pieces:
            self.board[p.row][p.col] = 0
            if p != 0:
                if p.color == WHITE:
                    self.remaining_w -= 1
                else:
                    self.remaining_b -= 1

    def winner(self):
        if self.remaining_b <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK

        return None

    def move_piece_on_board(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # In order to sketch the board properly, I'm creating a Piece object
                # according to the parity of the exact row (first row would have even squares pieces, 2nd
                # row would have odd squares pieces and so forth)
                if col % 2 == ((row + 1) %2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_valid_moves(self, piece):
        # moves will hold a key,value sets of target: current location of piece
        # e.g: (2,3): [(1,2)], where (2,3) is a valid move target square,
        # (1,2) is a location of a piece that is able to move to there
        moves = {}
        # Left diagonal
        col_to_the_left = piece.col - 1
        # Right diagonal
        col_to_the_right = piece.col + 1
        row = piece.row

        if piece.color == BLACK:
            # row-3 , because I'd like to watch the 2 rows above the current row at most.
            # 'left' is where the method will start for the column
            # and is the gap the method will subtract when moving
            # forward (up for the BLACK player).
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, col_to_the_left))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, col_to_the_right))
        if piece.color == WHITE:
            moves.update(self._traverse_left(row+1, min(row+3, ROWS), 1, piece.color, col_to_the_left))
            moves.update(self._traverse_right(row+1, min(row+3, ROWS), 1, piece.color, col_to_the_right))

        return moves

    # 'skipped' field exists for purpose of recursive calls after
    # skipping a rival piece in a previous call of the function.
    # 'left' is where do we start in terms of the column when we
    # traverse to the left
    def _traverse_left(self, start, stop, step, color, left_col_index, skipped=[]):
        moves = {}
        last = []
        for row in range(start, stop, step):
            if left_col_index < 0:
                break
            current = self.board[row][left_col_index]
            # If current square is free of pieces
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, left_col_index)] = last + skipped
                else:
                    moves[(row, left_col_index)] = last

                if last:
                    if step == -1:
                        stop = max(row - 3, 0)
                    else:
                        stop = min(row + 3, ROWS)
                    moves.update(self._traverse_left(row + step, stop, step, color, left_col_index - 1, skipped=skipped+last))
                    moves.update(self._traverse_right(row + step, stop, step, color, left_col_index + 1, skipped=skipped+last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left_col_index -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right_col_index, skipped=[]):
        moves = {}
        last = []
        for row in range(start, stop, step):
            if right_col_index >= COLS:
                break
            current = self.board[row][right_col_index]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, right_col_index)] = last + skipped
                else:
                    moves[(row, right_col_index)] = last

                if last:
                    if step == -1:
                        stop = max(row - 3, 0)
                    else:
                        stop = min(row + 3, ROWS)
                    moves.update(
                        self._traverse_left(row + step, stop, step, color, right_col_index - 1, skipped=skipped+last)
                    )
                    moves.update(
                        self._traverse_right(row + step, stop, step, color, right_col_index + 1, skipped=skipped+last)
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right_col_index += 1

        return moves
