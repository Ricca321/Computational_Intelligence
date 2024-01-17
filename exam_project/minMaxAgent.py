import random
from game import Game, Move, Player
from gameGym import GameGym
import randomAgent
from copy import copy
from copy import deepcopy
from collections import namedtuple
import numpy as np
from random import choice, randint
from tqdm import tqdm
from scipy.special import softmax
import pickle
import matplotlib.pyplot as plt



class GameNode:
    def __init__(self, current_game, move, available_moves, ply_id, parent = None) -> None:
        super().__init__()
        self.game = deepcopy(current_game)
        self.state = current_game.get_board()
        #add state value
        self.available_moves = available_moves
        self.children = []
        self.move = move
        self.parent = parent
        self.ply_id = ply_id
        self.value = 0

    def __add_children__(self, childNode):
        if childNode not in self.children:
            self.children.append(childNode)

    #@staticmethod
    def __get_available_moves(self, ply_id, current_board):
        table_index_valid = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
        flattened_board = [item for sublist in current_board for item in sublist]
        moves = []
        for i in table_index_valid:
            if flattened_board[i] != 1 - ply_id:
                if i<5:
                    moves.append((i - 5*(i//5), i//5, Move.BOTTOM)) #first row can go BOTTOM, e.g id = 14 -> (4,2) | x = 14 - 5*14/5 = 14 - 10 = 4
                                                                                                                #| y = 14/5 = 2
                if i%5 == 0:
                    moves.append((i - 5*(i//5), i//5, Move.RIGHT)) #first column can go RIGHT

                if i>19:
                    moves.append((i - 5*(i//5), i//5, Move.TOP)) #last row can go TOP
                
                if i%5 == 4:
                    moves.append((i - 5*(i//5), i//5, Move.LEFT)) #last column can go LEFT

        return moves
    
    def __compute_tree__(self):
        for move in self.available_moves:
            self.game.move((move[0], move[1]), move[2], self.ply_id)
            child = self.game.get_board()
            self.__add_children__(GameNode(self.game, move, self.__get_available_moves(self.ply_id, child),self.ply_id, self ))


    def __evaluate__(self, matrix, sign):
        # Controlla le righe 
        max_row_count = max([row.count(sign) for row in matrix]) 
    
        # Controlla le colonne 
        max_column_count = max([column.count(sign) for column in zip(*matrix)]) 
    
        # Controlla la diagonale principale 
        main_diagonal_count = sum([matrix[i][i] == sign for i in range(5)]) 
    
        # Controlla la diagonale secondaria 
        secondary_diagonal_count = sum([matrix[i][4-i] == sign for i in range(5)]) 
    
    
        return max(max_row_count, max_column_count, main_diagonal_count, secondary_diagonal_count)
    
class GameTree:
    def __init__(self, root) -> None:
        self.root = root
        current = root
        current.__compute_tree__()
        if len(current.children) > 0:
            for child in current.children:
                child.__compute_tree__()
                for grchild in child.children:
                    grchild.__compute_tree__()
                    

        
class minMaxPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.id = -1
        self.root = None# # GameNode
        self.game_tree = None #GameTree(self.root)  # GameTree

    
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        self.id = game.get_current_player()
        self.root = GameNode(GameGym(game.get_board()), None, self.__get_available_moves(self.id, game.get_board()), self.id,None) 
        self.game_tree = GameTree(self.root)
        node = self.alpha_beta_search(self.root)
        return (node.move[0], node.move[1]), node.move[2]

    def __get_available_moves(self, ply_id, current_board):
        table_index_valid = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
        flattened_board = [item for sublist in current_board for item in sublist]
        moves = []
        for i in table_index_valid: 
            if flattened_board[i] != 1 - ply_id: 
                if i<5: 
                    moves.append((i - 5*(i//5), i//5, Move.BOTTOM)) #first row can go BOTTOM, e.g id = 14 -> (4,2) | x = 14 - 5*14/5 = 14 - 10 = 4 
                                                                                                                #| y = 14/5 = 2 
                    if i!=0 and i!=4: 
                        moves.append((i - 5*(i//5), i//5, Move.LEFT) )
                        moves.append((i - 5*(i//5), i//5, Move.RIGHT) )
                         
                if i%5 == 0: 
                    moves.append((i - 5*(i//5), i//5, Move.RIGHT)) #first column can go RIGHT 
 
                    if i!=0 and i!=20: 
                        moves.append((i - 5*(i//5), i//5, Move.TOP) )
                        moves.append((i - 5*(i//5), i//5, Move.BOTTOM) )
 
                if i>19: 
                    moves.append((i - 5*(i//5), i//5, Move.TOP)) #last row can go TOP 
 
                    if i!=20 and i!=24: 
                        moves.append((i - 5*(i//5), i//5, Move.LEFT) )
                        moves.append((i - 5*(i//5), i//5, Move.RIGHT) )
                 
                if i%5 == 4: 
                    moves.append((i - 5*(i//5), i//5, Move.LEFT)) #last column can go LEFT 
 
                    if i!=0 and i!=20: 
                        moves.append((i - 5*(i//5), i//5, Move.TOP) )
                        moves.append((i - 5*(i//5), i//5, Move.BOTTOM))
        return moves

    def alpha_beta_search(self, node): # player has to maximize the opponent's states (which are minimized)
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        return best_state

    def max_value(self, node, alpha, beta):
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        return node.value
