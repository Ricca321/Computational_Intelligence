import random
from game import Game, Move, Player
from gameGym import GameGym
import randomAgent
from random import choice, randint
from scipy.special import softmax
import numpy as np
import math
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt
import tableState

TRAINING_PLAY_SIZE = 10000
LR = 0.3
DECAY = 5
EPSILON = 0.05
VALID_INDEX = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
BATCH = 100

class RLPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.epsilon = 1
        self.id = -1
        self.current_game = []
        self.table_state = tableState.TableState()
        
        

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
    def make_random_move(self, gameGym: GameGym, board):
            #Make random move if not present in list or exploring
            row = random.randint(0,4)
            column = random.randint(0,4)
            while board[row][column] == 1-self.id or not self.__check_border__((row,column),self.id, board):
                row = random.randint(0,4)
                column = randint(0,4)
            move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
            
               
            return  row, column, move
    
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        self.id = game.get_current_player()
        gameGym = GameGym(np.array(game.get_board()))
        current_board = game.get_board()
        

        if random.random() < self.epsilon:
            row, column, move = self.make_random_move(gameGym, current_board)
            if gameGym.slide((row, column), move) and gameGym.take((row, column), self.id):
                self.current_game.append((str(current_board),(row,column,move)))
            return (column, row), move
        else:
            row,column, move = self.__get__row_column_move__(str(current_board), gameGym, current_board)
            while game.get_board()[row][column] == 1-self.id:
                row,column, move = self.__get__row_column_move__(str(current_board), gameGym, current_board)             
          
        #add state to current_ board game
        if gameGym.slide((row, column), move) and gameGym.take((row, column), self.id):     
            self.current_game.append((str(current_board),(row,column,move)))
        return (column, row), move
    
    def __get__row_column_move__(self, state: str, gameGym, board):
            #flattened to use in random weighted
            table_points = [[(0,0) for _ in range(5)] for _ in range(5)]
            table_points[0][0] = (0, 0)
            table_points[0][4] = (0, 4)
            table_points[4][0] = (4, 0)
            table_points[4][4] = (4, 4)
            for i in range(1,4):
                        table_points[0][i] = (0, i)
                        table_points[4][i] = (4, i)
                        table_points[i][0] = (i, 0)
                        table_points[i][4] = (i, 4)
            flattened_table_points_table = [item for sublist in table_points for item in sublist]
            table_index_valid = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
            table_index = [i for i in  range(25)]
            #check if state present in table state
            tables = self.table_state.get_state(state)
            if tables == False:
                 return self.make_random_move(gameGym, board)
            else: 
                #if present use in prob_table fo that state
                table_prob, table_move_prob = tables[0], tables[1]
                probabilities = softmax([item for sublist in table_prob for item in sublist])
                
                #select cell from the border one
                table_element_index = np.random.choice(table_index, p=probabilities)
                while table_element_index not in table_index_valid:
                    table_element_index = np.random.choice(table_index, p=probabilities)

                table_element = flattened_table_points_table[table_element_index]
            
                moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
                row = table_element[1]
                column = table_element[0]

                move = np.random.choice(moves, p = softmax(table_move_prob[row][column]))
                return row, column, move
    
    

    def training(self):
        print("START TRAINING")
        self.__training_play__(self)
        print("TRAINING ENDED")
             
   
    def __stick_and_carrots__(self,winner):
        MUL = 0
        
        if winner == self.id: 
            MUL = 1
        else:
            MUL = -1
             
        for i, s in enumerate(self.current_game):
            t_state = self.table_state.get_state(s[0])
            if t_state == False:
                self.table_state.add_or_modify_state(s[0], None, None)
                t_state = self.table_state.get_state(s[0])
            row = s[1][0]
            column =s[1][1]
            
            table_prob = t_state[0]
            table_move_prob = t_state[1] 
            reward = 0.02 
            if (MUL == 1 and table_prob[row][column] < 1.0) or (MUL == -1 and table_prob[row][column] > 0.0):
                table_prob[row][column] =table_prob[row][column]+(MUL*reward)
                used_move = s[1][2] #((),(0,1,2))
                moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
                index_moves = moves.index(used_move)
                table_move_prob[row][column][index_moves] = table_move_prob[row][column][index_moves] +(MUL*reward)

                self.table_state.add_or_modify_state(s[0], table_prob, table_move_prob)
            self.current_game =[]
        
    def savePolicy(self):
        fw = open('policy', 'wb')
        pickle.dump(self.table_state, fw)
        fw.close()


    def loadPolicy(self, file1, file2):
            self.epsilon = 0
            fr = open(file1, 'rb')
            self.table_state = pickle.load(fr)
            fr.close()


    def __training_play__(self, agent):
            #Play 
            win_count = 0
            avg_win_hist =[]
            epsilon_hist=[]
            win_counter = 0
            batch = 0
           
            for i in  tqdm(range(TRAINING_PLAY_SIZE)):
                
                self.epsilon = 1* math.exp(-((i*DECAY)/(TRAINING_PLAY_SIZE-1)))
                epsilon_hist.append(self.epsilon)
                g = Game()
                player1 = agent
                player2 = randomAgent.RandomPlayer()
                winner = g.play(player1, player2)

                self.__stick_and_carrots__(winner)
                batch+=1
                
                if winner == self.id:
                    win_count+=1
                    win_counter+=1

                if batch == BATCH:
                    batch = 0
                    avg_win_hist.append((win_counter/(BATCH))*100)
                    win_counter = 0

            print((win_count/TRAINING_PLAY_SIZE)*100)
            print("SAVED POLICY")
            print("SAVED MOVE POLICY")
            print(self.table_state.get_state_len())
            self.savePolicy()
            self.__plotter__(epsilon_hist,avg_win_hist)
            self.table_state.print_table()
            return (win_count/TRAINING_PLAY_SIZE)*100
    
    
         

    def play_for_statistics(self):
        self.epsilon = 0
        win_count = 0
        self.loadPolicy("policy", "policy_move")
        self.table_state.print_table()
       
        for i in  tqdm(range(TRAINING_PLAY_SIZE)):
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

        episode = list(range(1, int(TRAINING_PLAY_SIZE/BATCH)+1))
        m, b = np.polyfit(episode, win, 1)
        y = m*np.array(episode)+b
        plt.plot(episode,y, marker='o', linestyle='-', color='b')
        plt.title('Win Rate')
        plt.xlabel('Episode')
        plt.ylabel('Win Rate') 
        plt.grid(True)
        plt.savefig('Win Rate')
        plt.show() 



        episode = list(range(1, int(TRAINING_PLAY_SIZE/BATCH)+1))
        plt.plot(episode,win, marker='o', linestyle='-', color='r')
        plt.title('Win Rate over Episode')
        plt.xlabel('Episode')
        plt.ylabel('Win Rate')
        plt.grid(True)
        plt.savefig('WINNING RATE')
        plt.show() 
