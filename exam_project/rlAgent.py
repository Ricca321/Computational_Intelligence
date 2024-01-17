import random
from game import Game, Move, Player
import randomAgent
from random import choice, randint
from scipy.special import softmax
import numpy as np
import math
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt

TRAINING_PLAY_SIZE = 10000
LR = 0.3
DECAY = 5
EPSILON = 0.05
VALID_INDEX = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
BATCH = 100

class RLPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.table_points: [[((int,int),Move,int)]]
        self.table_prob: [[float]]
        self.table_move_prob: [[[float]]]
        #self.index_table: [[(int, int)]]
        self.epsilon = 1
        self.id = -1
        
        

    def __check_border__(self, from_pos: tuple[int, int], player_id: int, board) -> bool:
        '''Take piece'''
        # acceptable only if in border
        acceptable: bool = (
            # check if it is in the first row
            (from_pos[0] == 0 and from_pos[1] < 5)
            # check if it is in the last row
            or (from_pos[0] == 4 and from_pos[1] < 5)
            # check if it is in the first column
            or (from_pos[1] == 0 and from_pos[0] < 5)
            # check if it is in the last column
            or (from_pos[1] == 4 and from_pos[0] < 5)
            # and check if the piece can be moved by the current player
        ) and (board[from_pos] < 0 or board[from_pos] == player_id)
        return acceptable   
     
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        self.id = game.get_current_player()
        if random.random() < self.epsilon:
            row = random.randint(0,4)
            column = random.randint(0,4)
            while game.get_board()[row][column] == 1-self.id or not self.__check_border__((row,column),self.id, game.get_board()):
                row = random.randint(0,4)
                column = randint(0,4)
            move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
            self.table_points[row][column] = (self.table_points[row][column][0], move, 1)
            return (column, row), move
        else:
            row,column, move = self.__get__row_column_move__()
            while game.get_board()[row][column] == 1-self.id:
                row,column, move = self.__get__row_column_move__()
                
            self.table_points[row][column] = ((row,column), move, self.table_points[row][column][2]+1)

        return (column,row), move
    
    def __get__row_column_move__(self):
            flattened_table_points_table = [item for sublist in self.table_points for item in sublist]
            table_index_valid = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
            table_index = [i for i in  range(25)]
            # Use softmax on the flattened list of probabilities
            probabilities = softmax([item for sublist in self.table_prob for item in sublist])
            # Use np.random.choice with the flattened list and probabilities
            table_element_index = np.random.choice(table_index, p=probabilities)
            while table_element_index not in table_index_valid:
                table_element_index = np.random.choice(table_index, p=probabilities)

            table_element = flattened_table_points_table[table_element_index]
           
            #tableElement  = np.random.choice(self.table_points, p = softmax(self.table_prob))
            moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
            row = table_element[0][1]
            column = table_element[0][0]
            move = np.random.choice(moves, p = softmax(self.table_move_prob[row][column]))
            return row, column, move
    
    def _init_table_points(self):
        self.table_points = [[((0,0),0,0) for _ in range(5)] for _ in range(5)]
        #self.index_table = [[(1,1) for _ in range(5)] for _ in range(5)]
        self.table_prob = [[0 for _ in range(5)] for _ in range(5)]
        self.table_move_prob = [[[0 for _ in range(4)] for _ in range(5)] for _ in range(5)]
        for i in range(5):
            self.table_prob[0][i] = random.random()
            self.table_prob[4][i] = random.random()
            self.table_prob[i][0] = random.random()
            self.table_prob[i][4] = random.random()
        """ for i in range(5):
            for j in range(5):
                print("[",self.table_prob[i][j],"]", end='')
            print("\n") """

        self.table_points[0][0] = ((0, 0), random.choice([Move.BOTTOM, Move.RIGHT]), 0)
        self.table_points[0][4] = ((0, 4), random.choice([Move.BOTTOM, Move.LEFT]), 0)
        self.table_points[4][0] = ((4, 0), random.choice([Move.TOP, Move.RIGHT]), 0)
        self.table_points[4][4] = ((4, 4), random.choice([Move.TOP, Move.LEFT]), 0)
        for i in range(1,4):
                    self.table_points[0][i] = ((0, i), random.choice([Move.BOTTOM, Move.LEFT, Move.RIGHT]), 0)
                    self.table_points[4][i] = ((4, i), random.choice([Move.TOP, Move.LEFT, Move.RIGHT]), 0)
                    self.table_points[i][0] = ((i, 0), random.choice([Move.TOP, Move.BOTTOM, Move.RIGHT]), 0)
                    self.table_points[i][4] = ((i, 4), random.choice([Move.TOP, Move.BOTTOM, Move.LEFT]), 0)
        '''for i in range(5):
            for j in range(5):
                print("[",self.table_points[i][j],"]", end='')
            print("\n")  '''
       
        self.table_move_prob[0][0] = [0,random.random(),0,random.random()]
        self.table_move_prob[0][4] = [0,random.random(),random.random(),0]
        self.table_move_prob[4][0] = [random.random(),0,0,random.random()]
        self.table_move_prob[4][4] = [random.random(),0,random.random(),0]
        for i in range(1,4):
                    self.table_move_prob[0][i] = [0, random.random(), random.random(), random.random()]
                    self.table_move_prob[4][i] = [random.random(),0, random.random(), random.random()]
                    self.table_move_prob[i][0] = [ random.random(), random.random(),0, random.random()]
                    self.table_move_prob[i][4] = [ random.random(), random.random(), random.random(),0]
        '''for i in range(5):
            for j in range(5):
                print("[",self.table_points[i][j],"]", end='')
            print("\n")  '''

    def training(self):
        self._init_table_points()
        print("START TRAINING")
        self.__training_play__(self)
        print("TRAINING ENDED")
             
    def __clear_point_table_picks__(self):
         for i in range(5):
            for j in range(5):
                self.table_points[i][j] = (self.table_points[i][j][0], self.table_points[i][j][1], 0)  

    def __stick_and_carrots__(self,winner, training):
        MUL = 0
        
        if winner == self.id: 
            MUL = 1
        else:
             MUL = -1
        for i in range(5):
            for j in range(5):
                #print(self.table_points[i][j])
                if  self.table_points[i][j][2] >= 1:
                    reward = ((MUL - self.table_prob[i][j])*LR)/self.table_points[i][j][2]
                    #reward = 1/(1+math.exp(-reward))
                    self.table_prob[i][j] = self.table_prob[i][j] + reward*training
                    used_move = self.table_points[i][j][1]
                    moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
                    index_moves = moves.index(used_move)
                 
                    self.table_move_prob[i][j][index_moves] = self.table_move_prob[i][j][index_moves] + reward*training
                    self.table_points[i][j] = (self.table_points[i][j][0], self.table_points[i][j][1], 0)   
        return reward
        
    def savePolicy(self):
        fw = open('policy', 'wb')
        pickle.dump(self.table_prob, fw)
        fw.close()
        fw = open('policy_move', 'wb')
        pickle.dump(self.table_move_prob, fw)
        fw.close()

    def loadPolicy(self,file1, file2):
            self._init_table_points()
            self.epsilon = 0
            fr = open(file1, 'rb')
            self.table_prob = pickle.load(fr)
            fr.close()

            fr = open(file2, 'rb')
            self.table_move_prob = pickle.load(fr)
            fr.close()

    def __training_play__(self, agent):
            
            win_count = 0
            avg_win_hist =[]
            epsilon_hist=[]
            win_counter = 0
            batch = 1

            for i in  tqdm(range(TRAINING_PLAY_SIZE)):
                self.epsilon = 1* math.exp(-((i*DECAY)/(TRAINING_PLAY_SIZE-1)))
                epsilon_hist.append(self.epsilon)
                g = Game()
                player1 = agent
                player2 = randomAgent.RandomPlayer()
                winner = g.play(player1, player2)
                #print("END BOARD")
                #g.print()
                #print(winner)
                self.__stick_and_carrots__(winner, 1)
                batch+=1
                
                if winner == self.id:
                    win_count+=1
                    win_counter+=1

                if batch == BATCH:
                    batch = 1
                    avg_win_hist.append((win_counter/(BATCH))*100)
                    win_counter = 0

                #print(self.table_points)
            print((win_count/TRAINING_PLAY_SIZE)*100)
            print("SAVED POLICY")
            #print(self.table_prob)
            print("SAVED MOVE POLICY")
            #print(self.table_move_prob)
            self.savePolicy()
            self.__plotter__(epsilon_hist,avg_win_hist)
            #print(avg_win_hist)
            return (win_count/TRAINING_PLAY_SIZE)*100

    def play_for_statistics(self):
        self._init_table_points()
        self.epsilon = 0
        #print(self.table_prob)
        win_count = 0
        self.loadPolicy("policy", "policy_move")
        #print(self.table_prob)
        for i in  tqdm(range(TRAINING_PLAY_SIZE)):
            self.__clear_point_table_picks__()
            g = Game()
            player1 = self
            player2 = randomAgent.RandomPlayer()
            winner = g.play(player1, player2)
            if winner == self.id:
                win_count+=1
        print((win_count/TRAINING_PLAY_SIZE)*100)

    def __plotter__(self,epsilon: list, win: list):
        episode =list(range(1, len(epsilon) + 1))
        plt.plot(episode,epsilon, marker='o', linestyle='-', color='b')
        plt.title('Epsilon Decay')
        plt.xlabel('Episode')
        plt.ylabel('Epsilon') 
        plt.grid(True)
        plt.savefig('EPSILON_DECAY')
        plt.show() 

        episode = list(range(1, int(TRAINING_PLAY_SIZE/BATCH) +1))
        plt.plot(episode,win, marker='o', linestyle='-', color='r')
        plt.title('Win Rate over Episode')
        plt.xlabel('Episode')
        plt.ylabel('Win Rate')
        plt.grid(True)
        plt.savefig('WINNING RATE')
        plt.show() 
