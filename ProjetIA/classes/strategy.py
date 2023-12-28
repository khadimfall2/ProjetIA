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
    def __init__(self, board_size):
    
        # Initialize the random player with the size of the board.
        
        self.board_size = board_size

    def select_tile(self, board):
        """
        Randomly selects a free tile on the board.

        :param board: the current game board
        :returns: (x, y) a tuple of integers corresponding to a valid and free tile on the board.
        """
        free_tiles = [(x, y) for x in range(self.board_size) for y in range(self.board_size) if board[x][y] == 0]
        return random.choice(free_tiles) if free_tiles else None


   
class MiniMax(PlayerStrat):
    def __init__(self, board_size, depth):
        """
        Initialize the MiniMax player with the size of the board and the depth of the search.

        :param board_size: Size of the board (e.g., 11 for an 11x11 board)
        :param depth: Depth of the MiniMax search tree
        """
        self.board_size = board_size
        self.depth = depth

    def select_tile(self, board, player):
        """
        Selects the best move using the MiniMax strategy.

        :param board: The current game board
        :param player: The player number (e.g., 1 or 2) for whom the move is being calculated
        :returns: (x, y) a tuple of integers corresponding to the best move
        """
        best_score = float('-inf')
        best_move = None

        for x in range(self.board_size):
            for y in range(self.board_size):
                if board[x][y] == 0:  # Check if the tile is free
                    board[x][y] = player  # Make a temporary move
                    score = self.minimax(board, self.depth - 1, False, player)
                    board[x][y] = 0  # Undo the move
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

    def minimax(self, board, depth, is_maximizing, player):
        """
        MiniMax algorithm implementation.

        :param board: The game board
        :param depth: Current depth of the search tree
        :param is_maximizing: Boolean indicating whether the current layer is maximizing or minimizing
        :param player: The player number
        :returns: The score of the board
        """
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
                        board[x][y] = 3 - player  # Switching to the other player
                        score = self.minimax(board, depth - 1, True, player)
                        board[x][y] = 0
                        best_score = min(best_score, score)
            return best_score

    def is_game_over(self, board):
        """
        Check if the game is over.

        :param board: The game board
        :returns: Boolean indicating whether the game is over
        """
        # Implement game over checking logic here
        # Placeholder: return False for now
        return False

    def evaluate_board(self, board, player):
        """
        Evaluate the board and return a score.

        :param board: The game board
        :param player: The player number
        :returns: A score representing the board's state
        """
        # Implement board evaluation logic here
        # Placeholder: return a random score for now
        return random.randint(-10, 10)

   
str2strat: dict[str, PlayerStrat] = {
        "human": None,
       # "random": Random,
       #"minimax": MiniMax,
}