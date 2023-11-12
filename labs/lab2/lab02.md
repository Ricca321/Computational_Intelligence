# Nim Game Playing

This repository contains a Nim game implementation where the agent learns how to play the game using a genetic algorithm. The agent's strategy is defined by a genotype, and its performance is evaluated against a specified opponent.

## Nim Game

Nim is a two-player mathematical game where players take turns removing objects from distinct heaps or piles. The game ends when a player removes the last object, and the last player to make a move wins.

## Agent

The agent is implemented using a genetic algorithm. The genotype of the agent defines its strategy, and the genetic algorithm evolves a population of agents over multiple generations to improve their performance in playing Nim.

### Genetic Algorithm Components

- **Initialization:** A population of agents with initialized genotypes is created.

- **Selection:** Agents are selected from the population based on their fitness, their success in playing against a specified opponent.

- **Mutation:** Some agents undergo mutation, where a random gene in their genotype is modified to introduce variability.

- **Crossover:** Other agents undergo crossover, where the genes from two parent agents are combined to create a new agent.

- **Evaluation:** The fitness of each agent is evaluated by playing multiple games of Nim against the opponent.

### Training

The training process involves multiple generations of evolution. The algorithm selects, mutates, and crosses over agents to create the next generation. This process continues until a specified number of generations is reached.


# Agent Strategy

The based agent strategy consists in taking the most amount of object from the bigger row.
The behaviour for each agent is encoded in its genotype, which consists of two parameters: `[parameter_1, parameter_2]`. These parameters influence the agent's decision-making during the Nim game, the first parameter rapresent the number that is going to be subtracted or added to the row, while the second paramenter referes to number that can be added or subtracted to the number of object that should be taken.

The strategy adopted is based on the total number of rows and tokens in the current state of the Nim game. The agent evaluates possible moves and selects the move that maximizes a combination of the row parameter and the token parameter in its genotype.

The strategy also includes considerations for edge cases, such as avoiding negative token values and ensuring that the selected row is within the valid range.

## Training Process

The training process involves multiple generations of evolving the agent population. Agents that perform well are sorted by fitness and the only the best agent will "survive" for the generation ("Natural Selection") 

## How to Experiment with Strategies

Users can experiment with different agent strategies by adjusting the initial genotype parameters, mutation rates, and other hyperparameters in the code. Observing the impact of these changes on the agent's performance provides insights into the dynamics of the learning process.

## Conclusion 
The agent with genotype [-2,-1] has a winning rate on avarage of 36% against the optimal algorithm.
![Fitness of Agent vs Optimal over generation](https://github.com/Ricca321/Computational_Intelligence/blob/main/labs/lab2/images/learning.jpeg)
![Win rates of 1000 matches divided in 100 games batches](https://github.com/Ricca321/Computational_Intelligence/blob/main/labs/lab2/images/winrate.jpeg)

## Contributing
Made with the contribuition of Andrea Sillano s314771
