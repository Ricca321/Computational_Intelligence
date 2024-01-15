# Project Exam: QUIXO

## Introduction

This project represents two possible implementation of algorithms for playing Quixo, a strategic board game.

## Game Rules

Quixo is a two-player board game played on a 5x5 grid. Each player has a set of pieces and can either move a piece on the grid or slide an entire row or column of the grid. The objective is to align 5 pieces of the same shape (X or O) in a row, column, or diagonal.

## Introduction on the algorithm leveraged

We tried to implement two different types of algorithm based on ES and RL:
- **Evolutionary Strategy**, tries to obtain the best agent by maximizing the fitness. It selects a move depending on a probability, it can decide to mirrow the opponent or to do a greedy choice;
- **Reinforcement Learning**, tries to learn the best state. The moves are selected based on a score_table taking the most promising one at every turn;

## ES algorithm

### Agent

The agent is implemented using a genetic algorithm. The genotype of the agent defines its strategy, and the genetic algorithm evolves a population of agents over multiple generations to improve their performance in playing Quixo.
Here the genotype is composed by a tuple representing two probabilities and a vector of four probabilities representing the probabilities of the move direction (TOP, BOTTOM, LEFT, RIGHT). About the tuple, we split the game in two different parts; the first when there are still empty places and the second when you can only moves your tiles. The probabilites represent the likelihood of selecting the mirror or the greedy make_move.

#### Genetic Algorithm Components

- **Initialization:** A population of agents with initialized genotypes is created.

- **Selection:** Agents are selected from the population based on their fitness, their success in playing against a specified opponent.

- **Mutation:** Some agents undergo mutation, where genes in their genotype is modified to introduce variability. In particular we mutate the four probabilities of the directions

- **Crossover:** Other agents undergo crossover, where the genes from two parent agents are combined to create a new agent.

- **Evaluation:** The fitness of each agent is evaluated by playing multiple games of Quixo against the opponent.

#### Training

The training process involves multiple generations of evolution. The algorithm selects, mutates, and crosses over agents to create the next generation. This process continues until a specified number of generations is reached. Agents that perform well are sorted by fitness and the only the best agent will "survive" for the generation ("Natural Selection").

### Agent Strategy

The based agent strategy consists of two different strategies depending on the relative probability. It can make a move mirroring the opponent or in a greedy selection:

- **mirror_stategy**: it selects the last opponent's move and rotate it. If this is the first move it will take a random move;
- **greedy_stategy** it selects the row/column/diagonal with the biggest number of tiles with own shapes;

### How to Experiment with Strategies

Users can experiment with different agent strategies by adjusting the initial genotype parameters, mutation rates, and other hyperparameters in the code. Observing the impact of these changes on the agent's performance provides insights into the dynamics of the learning process.

### Conclusion 

## RL algorithm

The reinforcement learning strategy evolves over time based on the outcomes of games, adjusting its approach using a reward system.

### Strategy

The reinforcement learning process involves assigning and updating values to different positions on the game board. These values represent the desirability of making a move in a particular position, and they are adjusted based on the game's outcomes.
In particular, we used the following approach:
- _reinforcement_strategy_: The player has a game_table where every position has an associated point and status (the higher the score, the higher the probability to be chosen as next move). These scores are randomly initialized with a value between 0 and 1. It is introduced an exploration approach based on epsilon-greedy. During the learning phase, with a probability of **EPSILON**, the player will make a random move to explore new possibilities. Otherwise, it will choose the move that maximizes the current value of the learning strategy. The **EPSILON** value has a decay rate of N = N_0*e^-((i * decay)/GAME_SIZE - 1) where i is the current episode (episode = game). The selection of the next move will be based on the position with maximize the sum of the set (where the set is composed by all the previous taken positions)

#### Reward system

Every game in **practice** is evaluated using _stick_and_carrot_: this function implements the reward system based on the outcome of the game.
The parameters of the system are:
- MUL: used to discriminate between **WIN**, **LOSE**, **DRAW**
- LR: it is a multiplier used to dimension the reward

The formula used to compute the reward is: reward = (MUL - table_points[pos_x][pos_y]) * LR

The computed reward is added to the previous table_score[pos_x][pos_y] only if the player has chosen this position. This method allows the player to reward the winning set while penalized the loosing set.

#### Plot

At the end two plot are given:
- _EPSILON_Decay_: We used an exponential decay. It starts from 1 with a decay = 5
![]()
- _Winning_Rate_: In the practice phase we divided all the games in batches of 5000 episodes on which the winning_rate is computed
![]()

#### Save and Load Policy

Once the training is finished, it is possible to store in a file the policy composed by the updated table_points in order to reuse those scores in the next executions without retraining the agent by loading the policy

- _Save_policy_: it allows the user to save the policy in a file

- _Load_policy: it allows the user to load the policy from a file

### Conclusion

## Contribution
Made with the contribuition of Andrea Sillano s314771
