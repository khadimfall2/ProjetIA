import copy
import math
import random
from math import log, sqrt, inf
from random import randrange
import numpy as np
from rich.table import Table
from rich.progress import track
from rich.console import Console
from rich.progress import Progress

import classes.logic as logic

# When implementing a new strategy add it to the `str2strat`
# dictionary at the end of the file


class PlayerStrat:
    def __init__(self, _board_state, player):
        self.root_state = _board_state
        self.player = player

    def start(self):
        """
        This function select a tile from the board.

        @returns    (x, y) A tuple of integer corresponding to a valid
                    and free tile on the board.
        """
        raise NotImplementedError

class Node(object):
    """
    This class implements the main object that you will manipulate : nodes.
    Nodes include the state of the game (i.e. the 2D board), children (i.e. other children nodes), a list of
    untried moves, etc...
    """
    def __init__(self, board, move=(None, None),
                 wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = board
        self.move = move
        self.wins = wins
        self.visits = visits
        self.children = children or []
        self.parent = None
        self.untried_moves = logic.get_possible_moves(board)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class RandomPlayer(PlayerStrat):
    def __init__(self, _board_state, player):
        super().__init__(_board_state, player)
        self.board_size = len(_board_state)

    def select_tile(self, board):
        """
        Randomly selects a free tile on the board.

        :param board: the current game board
        :returns: (x, y) a tuple of integers corresponding to a valid and free tile on the board.
        """
        free_tiles = [(x, y) for x in range(self.board_size) for y in range(self.board_size) if board[x][y] == 0]
        return random.choice(free_tiles) if free_tiles else None
        def start(self):
         return self.select_tile(self.root_state)
    def start(self):
      return self.select_tile(self.root_state)



   
    
    # Définition de la classe MiniMax
class MiniMax(PlayerStrat):
    def __init__(self, _board_state, player, depth=2):
        super().__init__(_board_state, player)
        self.board_size = len(_board_state)
        self.depth = depth

    def select_tile(self, board, player):
        best_score = float('-inf')
        best_move = None

        for x in range(self.board_size):
            for y in range(self.board_size):
                if board[x][y] == 0:
                    board[x][y] = player
                    score = self.minimax(board, self.depth - 1, False, player)
                    board[x][y] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

    def minimax(self, board, depth, is_maximizing, player):
        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board, player)

        if is_maximizing:
            best_score = float('-inf')
            for x in range(self.board_size):
                for y in range(self.board_size):
                    if board[x][y] == 0:
                        board[x][y] = player
                        score = self.minimax(board, depth - 1, False, player)
                        board[x][y] = 0
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for x in range(self.board_size):
                for y in range(self.board_size):
                    if board[x][y] == 0:
                        board[x][y] = 3 - player
                        score = self.minimax(board, depth - 1, True, player)
                        board[x][y] = 0
                        best_score = min(best_score, score)
            return best_score

    def is_game_over(self, board):
        return logic.is_game_over(self.player, board) is not None

    def evaluate_board(self, board, player):
        if logic.is_game_over(player, board):
            return 10
        elif logic.is_game_over(3 - player, board):
            return -10
        else:
            return 0

    def start(self):
        return self.select_tile(self.root_state, self.player)

    


   
str2strat: dict[str, PlayerStrat] = {
        "human": None,
        "random": RandomPlayer,
        "minimax": MiniMax,
}