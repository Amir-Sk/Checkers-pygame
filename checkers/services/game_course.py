import pygame
from services.constants import BLACK, BLUE, SQUARE_SIZE, WHITE, YELLOWISH, RADIUS
from model.board import Board


class GameCourse(object):

    center_delta = SQUARE_SIZE // 2

    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.selected_piece = None
        self.turn = BLACK
        self.valid_moves = {}
        self._init_game()

    def reset(self):
        self._init_game()

    def select(self, row, col):
        if self.selected_piece:
            did_piece_moved = self._move(row, col)
            if not did_piece_moved:
                self.selected_piece = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected_piece and piece == 0 and (row, col) in self.valid_moves:
            self.board.move_piece_on_board(self.selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_players_turn()
        else:
            return False
        return True

    def change_players_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def update(self):
        self.board.draw(self.win)
        self.show_valid_moves_on_board(self.valid_moves)
        pygame.display.update()

    def _init_game(self):
        self.selected_piece = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def show_valid_moves_on_board(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win,
                YELLOWISH,
                (col * SQUARE_SIZE + self.center_delta,
                 row * SQUARE_SIZE + self.center_delta),
                RADIUS
            )
