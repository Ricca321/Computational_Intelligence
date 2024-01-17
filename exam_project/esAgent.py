import random
from game import Game, Move, Player
import randomAgent
from copy import copy
from collections import namedtuple
import numpy as np
from random import choice, randint
from tqdm import tqdm
from scipy.special import softmax
import pickle
import matplotlib.pyplot as plt
import math
GENERATION_SIZE = 50
TOURNAMENT_SIZE = 10
POPULATION_SIZE = 100
OFFSPRING_SIZE = 20
EPSILON = 0.15
MUTATION = 0.1
TRAINING_PLAY_SIZE = 100


class EsPlayer(Player):
   
    def __init__(self) -> None:
        super().__init__()
        self.status =(random.random(),random.random())
        self.fitness = 0.0
        self.opponent_moves = []
        self.moves_probability = [random.random(),random.random(),random.random(),random.random()] #np.random.rand( 4)
        self.greedy_counter = 0
        self.mirror_counter = 0
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
    
    def __mirror_strategy__(self, last_move, board):
        self.mirror_counter +=1
        #print("MIRROR")
        #from_pos = (random.randint(0, 4), random.randint(0, 4))
        #move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        #return from_pos, move
        frompos = (last_move[0], last_move[1]) 
        new_row = 0
        new_column = 0
        if board[frompos[1]][frompos[0]]  == 1-self.id or not self.__check_border__(frompos, self.id, board):
            #if last_move[1] != 0:
            new_row  = randint(0,4)
            #if last_move[0] != 0:
            new_column = randint(0, 4)
            frompos = (new_row, new_column)
            #print("Impossible")
        moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
        #move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        move = np.random.choice(moves, p = softmax(self.moves_probability))
        return frompos, move
    
    def __greedy_startegy__(self, board):
        #print("GREEDY")
        self.greedy_counter +=1
        #ROWS
        max_row = -1
        for i in range(5):
            curren_max = 0
            for j in range(5):
               if board[i][j] == self.id:
                    curren_max+=1
            if curren_max > max_row:
                max_row = i

        # COLUMNS
        max_column = -1
        for i in range(5):
            curren_max = 0
            for j in range(5):
               if board[j][i] == self.id:
                    curren_max+=1
            if curren_max > max_column:
                max_column = i
        
        if max_column >max_row:
            if board[0][max_column] != 1-self.id:
                return (max_column,0), Move.BOTTOM
            elif board[4][max_column] != 1-self.id:
                return (max_column,4), Move.TOP
        else:
            if board[max_row][0] != 1-self.id:
                return (0,max_row), Move.RIGHT
            elif board[max_row][4] != 1-self.id:
                return (4,max_row), Move.LEFT
            
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        moves = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
        #move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        move = np.random.choice(moves, p = softmax(self.moves_probability))
        return from_pos, move

                
    def __check_already_in_list__(self, board):
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 1-self.id and (i,j) not in self.opponent_moves:
                        self.opponent_moves.append((i,j))

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        self.id = game.get_current_player()
        game_board = game.get_board().tolist()
        self.__check_already_in_list__(game_board)
        status =  0 if any(element == -1 for element in game_board) else 1
        if random.random() < self.status[status]:
            if len(self.opponent_moves) == 0:
                from_pos = (random.randint(0, 4), random.randint(0, 4))
                move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
                return from_pos, move
            else:
                from_pos, move = self.__mirror_strategy__(self.opponent_moves[-1], game.get_board())
                return from_pos, move
        else:
            #print("GREEDY")
            from_pos, move = self.__greedy_startegy__(game.get_board())
            return from_pos,move
    
    def __mutate__(self, agent):
        offspring = copy(agent)
        new_before_threshold = np.random.normal(offspring.status[0], MUTATION)
        new_after_threshold = np.random.normal(offspring.status[1], MUTATION)
        new_moves_probability = []
        for i in range(len(self.moves_probability)):
            new_moves_probability.append(np.random.normal(offspring.moves_probability[i], MUTATION))
        offspring.status = (new_before_threshold, new_after_threshold)
        offspring.moves_probability = new_moves_probability

        return offspring
    
    def __select_parent__tournament__(self, population):
        pool = [choice(population) for _ in range(TOURNAMENT_SIZE)]
        champion = max(pool, key=lambda i: i.fitness)
        return champion
    
    def savePolicy(self,agent):

        fw = open('policyES', 'wb')
        pickle.dump(agent, fw)
        fw.close()
       

    def loadPolicy(self,file1):
            fr = open(file1, 'rb')
            agent = pickle.load(fr)
            self.status = agent.status
            self.id = agent.id
            self.moves_probability = agent.moves_probability
            fr.close()

            #print(self.fitness)
            #print(self.moves_probability)
    def __xover__(self, p1 , p2):
        offspring = copy(p1)
        gene_from_p1 = randint(0, 1)
        gene_from_p2 = 1-gene_from_p1
        offspring.status = (p1.status[gene_from_p1], p2.status[gene_from_p2])
        mutation_prob_rate = [random.random() for _ in range(4)]
        offspring.moves_probability = [p1 if r < .5 else p2 for p1, p2, r in zip(p1.moves_probability, p2.moves_probability, mutation_prob_rate)]
        return offspring

    def training(self):
        population = self.__init_population__()
        fitness_list = []
        print("STARTING TRAINING")
        for _ in tqdm(range(GENERATION_SIZE)):
            offspring = []
            for i in range(OFFSPRING_SIZE):
                if random.random() < MUTATION:
                    agent = self.__select_parent__tournament__(population)
                    agent = self.__mutate__(agent)
                else:
                    agent1 = self.__select_parent__tournament__(population)
                    agent2 = self.__select_parent__tournament__(population)
                    agent = self.__xover__(agent1,agent2)
                offspring.append(agent)
            for agent in offspring:
                 agent.fitness = self.__training_play__(agent)
            population.extend(offspring)
            population.sort(key=lambda i: i.fitness, reverse=True)
            population = population[:POPULATION_SIZE]
            fitness_list.append(population[0].fitness)
            print(population[0].fitness)
        print("POLICY SAVED!")
        self.savePolicy(population[0])
        self.__plotter__(fitness_list)
        print(population[0])
            
        

    def __init_population__(self):
        population = [EsPlayer() for _ in range(POPULATION_SIZE)]
        print("INITIALIZING POPULATION!")
        for agent in tqdm(population):
            agent.fitness = self.__training_play__(agent)
        population.sort(key=lambda i: i.fitness, reverse=True)
        return population

    def __training_play__(self, agent):
        win_count = 0

        for _ in range(TRAINING_PLAY_SIZE):
            g = Game()
            player1 = agent
            player2 = randomAgent.RandomPlayer()
            winner = g.play(player1, player2)
            #print("END BOARD")
            if winner == agent.id:
                win_count+=1
        
        return (win_count/TRAINING_PLAY_SIZE)*100

    def play_for_statistics(self):
        #print(self.table_prob)
        win_count = 0
        self.loadPolicy("policyES")
       
        for i in  tqdm(range(TRAINING_PLAY_SIZE)):
            g = Game()
            player1 = self
            player2 = randomAgent.RandomPlayer()
            winner = g.play(player1, player2)
            if winner == self.id:
                win_count+=1
        print((win_count/TRAINING_PLAY_SIZE)*100)

    def __plotter__(self,fitness_list: list):
        generations = list(range(1, len(fitness_list) + 1))
        plt.plot(generations, fitness_list, marker='o', linestyle='-', color='b')
        plt.title('Fitness Over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.grid(True)
        plt.savefig('ES_FITNESS')
        plt.show()
