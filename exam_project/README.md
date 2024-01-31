# Project Exam: QUIXO

## Introduction

This project represents three possible implementation of algorithms for playing Quixo, a strategic board game.

## Game Rules

Quixo is a two-player board game played on a 5x5 grid. Each player can either move a piece on the grid or slide an entire row or column of the grid. The objective is to align 5 pieces of the same shape (X or O) in a row, column, or diagonal.

## Introduction on the algorithm leveraged

We tried to implement three different types of algorithm based on ES, RL and MinMax:
- **Evolutionary Strategy**, tries to obtain the best agent by maximizing the fitness. It selects a move depending on a probability, it can decide to mirrow the opponent or to do a greedy choice;
- **Reinforcement Learning**, tries to find the best policy to win the game. The moves are selected based on a score_table of that state taking the most promising one at every turn;
- **MinMax Algorithm**, reduced version in deepth of minmax algorithm with alpha-beta pruning 

## ES algorithm

### Agent

The agent is implemented using a genetic algorithm. The genotype of the agent defines its strategy, and the genetic algorithm evolves a population of agents over multiple generations to improve their performance in playing Quixo.
Here the genotype is composed by a tuple representing two probabilities and a vector of four probabilities representing the probabilities of the move direction (TOP, BOTTOM, LEFT, RIGHT). About the tuple, we split the game in two different parts; the first when there are still empty places and the second when you can only moves your tiles. The probabilites represent the likelihood of selecting the mirror or the greedy make_move.

#### Genetic Algorithm Components

- **Initialization:** A population of agents with initialized genotypes is created.

- **Selection:** Agents are selected from the population based on their fitness, their success in playing against a specified opponent.

- **Mutation:** Some agents undergo mutation, where genes in their genotype is modified to introduce variability. In particular we mutate the tuple of status and the four probabilities of the directions

- **Crossover:** Other agents undergo crossover, where the genes from two parent agents are combined to create a new agent.

- **Evaluation:** The fitness of each agent is evaluated by playing multiple games of Quixo against the opponent.

#### Training

The training process involves multiple generations of evolution. The algorithm selects, mutates, and crosses over agents to create the next generation. This process continues until a specified number of generations is reached. Agents that perform well are sorted by fitness and the only the best agent will "survive" for the generation ("Natural Selection").

### Agent Strategy

The agent strategy consists of two different strategies depending on the relative probability; every agent has two probability for selecting the strategy (tuple), if there aren't available tiles it will select the second (status[1]), otherwise the first one. It can make a move mirroring the opponent or in a greedy selection:

- **mirror_stategy**: it selects the last opponent's move and rotate it. If this is the first move it will take a random move;
- **greedy_stategy** it selects the row/column/diagonal with the biggest number of tiles with own shapes;

#### How to Experiment with Strategies

Users can experiment with different agent strategies by adjusting the initial genotype parameters, mutation rates, and other hyperparameters in the code. Observing the impact of these changes on the agent's performance provides insights into the dynamics of the learning process.

### Conclusion 

After the training, the best agent reached a fitness value of 80%.
Although this result seems promising in the real game it is run dependent. By playing multiple batches of 100 games, the score varies from 54% to 72%.
The grafic below shows the fitness over training.
![](https://github.com/Ricca321/Computational_Intelligence/blob/main/exam_project/images/fitness.png)


## RL algorithm

The reinforcement learning strategy evolves over time based on the outcomes of games, adjusting its approach using a reward system.

### Strategy

The reinforcement learning process involves assigning and updating values to different positions on the game board.
More in detail, RL strategy uses a table state records which stores a game board related to a particular state.
The values on the board represent the desirability of making a move in a particular position, and they are adjusted based on the game's outcomes.
In particular, we used the following approach:
- _reinforcement_strategy_: The player has a list of states, used only in the reward phase to record the sequence of the game states, that unfold during the current game. Each state has the current game_board , the selected cell and the selected move . In every step of the game, if the exploration strategy isn't selected, the agent checks the table state records and if it contains the current state it uses both the table_prob and table_move_prob probabilities (using softmax) to choose the next move. Otherwise if the state isn't present in the records or the exploration is selected, a random move is chosen. These scores are initialized in a fixed way with a value of 0.1. It is introduced an exploration approach based on epsilon-greedy. During the learning phase, with a probability of **EPSILON**, the player will make a random move to explore new possibilities. Otherwise, it will choose the move that maximizes the current value of the learning strategy. The **EPSILON** value has a decay rate of N = N_0*e^-((i * decay)/(GAME_SIZE - 1)) where i is the current episode (episode = game).

Hence, in every step of the game the agent looks if the current state is present in the table state list (via hash) and if it finds the state it uses the probability_boards (one for cell and one for direction) to select the next movement (with higher softmax probabilities)

#### Reward system

Every game in **practice** is evaluated using _stick_and_carrot_: this function implements the reward system based on the outcome of the game.
The parameters of the system are:
- MUL: used to discriminate between **WIN**, **LOSE**

The reward is fixed to +0.02 for a win and -0.02 for a lost

The reward is then added to the selected table_probabilities table_prob[pos_x][pos_y], table_move_prob[pos_x][pos_y] of every state in that game only if the player has chosen this position. A list of tuples is kept to represent the sequence of the states in that game. In the tuple there is the game_board and a triple with the selected cell and the enumerator MOVE (row, column, MOVE) in order to modify only a value on the table_probabilities for a given state. This method allows the player to reward the winning set while penalized the loosing set.

#### Plot

At the end two plot are given:
- _EPSILON_Decay_: We used an exponential decay. It starts from 1 with a decay = 5
![](https://github.com/Ricca321/Computational_Intelligence/blob/main/exam_project/images/EPSILON_DECAY.png)
- _Winning_Rate_: In the practice phase we divided all the games in batches of 100 episodes on which the winning_rate is computed. After this the results are linearly interpolated in order to get a clear view 
![](https://github.com/Ricca321/Computational_Intelligence/blob/main/exam_project/images/Win%20Rate.png)

#### Save and Load Policy

Once the training is finished, it is possible to store in a file the policy composed by the list of state with table_prob and table_move_prob in order to reuse those scores in the next executions without retraining the agent by loading the policy

- _Save_policy_: it allows the user to save the policy in a file

- _Load_policy: it allows the user to load the policy from a file

### Conclusion
RL agent gets an average score of 55% on the last batch and in particular it seems to train itself as shown in the previous graph (section plot). The winrate on the batches passes from 50% to 55%.
This strategy allows the agent to not have a fixed approach related to the state but it depends on the softmax probabilities both for direction and cell selection.
Moreover, in the training we compute a reduced number of states in order to avoid the policy to become excessively large and too much slow in computation (with 10000 games there are more than 200k states and the policy is 200 MB)

## MinMax

We also implement MinMax algorithm with alpha-beta pruning, a decision-making algorithm used in two-player games. We already expect minmax to overcome other methods, so we will use it as a comparator for ES and RL. The code defines classes for the game, game tree nodes, and a MinMax player.

### Tree Management

- GameNode Class: The GameNode class represents nodes in the game tree. Each node contains information about the current game state, available moves, and a reference to its parent and children nodes. In particular the value is computed with a formula considering max number of player's tiles in a row, column or diagonal (from the search space of every row, column and diagonal) minus max number of opponent's tiles in a row, column or diagonal

- GameTree Class: The GameTree class is responsible for managing the game tree. It initializes with a root node and expands the tree by generating a child node for each move. The obtained tree will not contain all the possible states but only a subset (pruning, starting from the root, the tree will have a depth of two, children and granchildren)

### MinMax Algorithm Usage

- minMaxPlayer Class: This class extends the Player class and implements the MinMax algorithm for decision-making.

- Alpha-Beta Pruning: The alpha_beta_search function employs the MinMax algorithm with alpha-beta pruning. It evaluates potential moves to find the one with the maximum utility for the current player while minimizing the opponent's utility. Alpha-beta pruning is used to eliminate branches that won't affect the final decision, improving efficiency.

- Tree Traversal: The MinMax algorithm traverses the game tree by recursively exploring possible moves and their outcomes. The max_value and min_value functions represent the maximizing and minimizing steps in the algorithm. In particular we limit the exploration to 2 consecutive moves. So apart from root, we have child and granchild. MinMax in this case will take the value of granchildren, for every child it minimize its granchildren and in the end take the maximum child 

### Conclusion
After multiple runs the average winrate of MinMax agent is 80% which proves to be the most effective strategy among the proposed ones.
![](https://github.com/Ricca321/Computational_Intelligence/blob/main/exam_project/images/minmaxbatches.png)

## General and Final Considerations

Note: the winrate is related to the value specified in the column and it is obteined as the average on multiple runs of 100 games batches
|  | Random|  ES | RL | MinMax|
:-------------------------:|:-------------------------: |:-------------------------:|:-------------------------:|:-------------------------:|
| __Random__ | x | 60% | 55% | 78%  | 
| __ES__ | 42% | x | 52%| 84% | 
| __RL__| 52% | 61%| x | 84%| 
| __MinMax__ |25% | 20% | 23% | x | 

As we expected, MinMax gets the best performance against Random Player and also the other methods thanks to its ability to compute the next states, thus choosing the best move using the heuristic explained before.
Unexpectedly ES seems to be quite effective both against RL and Random.
On the other hand, the results of RL agent are biased due to the dimension of the computed state space; It should be trained more in order to compute a larger set of states thus obtaining better results. To increase the performances both of ES and RL models could be trained switching the starting agent.

## Contribution
Made with the contribuition of Andrea Sillano s314771
