# LAB10

The provided program implements a Tic-Tac-Toe game with a focus on reinforcement learning strategies. Tic-Tac-Toe is a two-player game played on a 3x3 grid, where players take turns marking a space with their symbol ("X" or "O"), and the first player to form a line of three symbols wins.

The primary objective of the code is to explore and demonstrate reinforcement learning techniques in the context of playing Tic-Tac-Toe. Reinforcement learning involves training an agent to make decisions by interacting with an environment and receiving feedback in the form of rewards or penalties.

## Key components

### TicTacToe Class:

The TicTacToe class encapsulates the game logic, including board initialization, move execution, and checking for a winning condition. It provides the foundation for player interaction. Also, it prints the game board.

### Player Strategies:

The code defines different player strategies, including a random strategy and a reinforcement learning strategy. The reinforcement learning strategy evolves over time based on the outcomes of games, adjusting its approach using a reward system.

### Reinforcement Learning:

The reinforcement learning process involves assigning and updating values to different positions on the game board. These values represent the desirability of making a move in a particular position, and they are adjusted based on the game's outcomes.
In particular, we used the following approach:
- _reinforcement_strategy_: The player has a game_table where every position has an associated point and status (the higher the score, the higher the probability to be chosen as next move). These scores are randomly initialized with a value between 0 and 1. It is introduced an exploration approach based on epsilon-greedy. During the learning phase, with a probability of **EPSILON**, the player will make a random move to explore new possibilities. Otherwise, it will choose the move that maximizes the current value of the learning strategy. The **EPSILON** value has a decay rate of N = N_0*e^-((i * decay)/GAME_SIZE - 1) where i is the current episode (episode = game). The selection of the next move will be based on the position with maximize the sum of the set (where the set is composed by all the previous taken positions)

### Training and Evaluation:

The code includes functions for practicing reinforcement learning (**practice**) and evaluating the performance of the reinforcement learning player against a random strategy (**real_game**). The win rate is calculated to assess the effectiveness of the learned strategy.

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
![](https://github.com/Ricca321/Computational_Intelligence/blob/main/labs/lab10/images/eps_decay.jpeg)
- _Winning_Rate_: In the practice phase we divided all the games in batches of 5000 episodes on which the winning_rate is computed
![](https://github.com/Ricca321/Computational_Intelligence/blob/main/labs/lab10/images/win_rate.jpeg)

#### Save and Load Policy

Once the training is finished, it is possible to store in a file the policy composed by the updated table_points in order to reuse those scores in the next executions without retraining the agent by loading the policy

- _Save_policy_: it allows the user to save the policy in a file

- _Load_policy: it allows the user to load the policy from a file

### Human vs. AI Interaction:

The code allows for human interaction with the AI player (**game_vs_human**). The player can make moves and play against a reinforcement learning-based AI, providing an interactive experience.

#### Input Handling:

The _InputHandler_ class is used to handle user input during human vs. AI gameplay: a new thread is initialized in order to properly control the execution of the while. When the human's move is required the thread handle the input putting in wait the program until the move is given. After that, the game is resumed and so on.

## Conclusion:
In summary, the code serves as an exploration of reinforcement learning techniques in the context of Tic-Tac-Toe. It demonstrates how an AI player can learn and adapt its strategy through reinforcement, and it provides avenues for evaluating and interacting with the trained agent. Our implementation tries to find the optimal positions to win the game; since it is not a complete Montecarlo strategy (because it does not generate all the possible states), it suffers against a real player because it can't block his/her moves.
In the end our model reaches good performances against a random model (about 70% win rate), this proves that the reinforcement learning technique is able to find an "optimal" strategy to win in most of the cases.

## Contribution
Made with the contribuition of Andrea Sillano s314771