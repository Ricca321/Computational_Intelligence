# LAB09

This program implements an evolutionary algorithm based on Evolution Strategies (ES) to solve an abstract problem based on one max.

### Definition of Parent Selection Functions:

parent_selection: Implements a tournament among random individuals from the population and returns the best one based on fitness.

### Definition of Genetic Operators:

xover: Implements the crossover (recombination) operator between two parents.
mutateRandom: Implements a mutation operator that randomly changes a bit in the individual's genotype.
mutateFlip: Implements a mutation operator which flips randomly a bit in the Individual's genotype.
mutate: Implements a mutation operator that randomly select a bit in the individual's genotype and set it to 1.
one_cut_xover: Implements a variant of crossover called "one-cut crossover."


### Implementation of Adaptive Strategies for Mutation and Crossover:

Based on the article [Choosing Mutation and Crossover Ratios for Genetic Algorithms—A Review with a New Dynamic Approach](https://www.mdpi.com/2078-2489/10/12/390) we decided to implement a variable probability both for mutation and crossover, in particular we have chosen:

**Dynamic Increasing of Low Mutation/Decreasing of High Crossover (ILM/DHC)**: Implements an adaptation strategy for mutation and crossover based on the current generation

**Dynamic Decreasing of High Mutation Rate/Increasing of Low Crossover Rate (DHM/ILC)**: Implements an adaptation strategy for mutation and crossover based on the current generation

Both of the strategies linearly change crossover and mutation rate based on the following formulas:

## ILM/DHC
- **MR = LG / GN** 
- **CR = 1 - MR**
- where:
    - GN = [0, 1, 2, ..., GENERATION_SIZE]
    - LG = CURRENT_GENERATION

## DHM/ILC

- **CR = LG / GN** 
- **MR = 1 - CR**
- where:
    - GN = [0, 1, 2, ..., GENERATION_SIZE]
    - LG = CURRENT_GENERATION

In order to compare the performances of the previous strategies, we also adopted static probabilities (**MR = 0.2** and **CR = 0.8**)

### ES Algorithm (μ + λ):

The _mu_plus_lambda_ function runs the ES algorithm with the "(μ + λ)" approach. It uses an iterative process of selection, crossover, and mutation to create a new population. The resulting population is then sorted based on fitness, and only the best individuals are retained.


### ES Algorithm (μ , λ):

The _mu_comma_lambda function_ runs the ES algorithm with the "(μ , λ)" approach. Similar to _mu_plus_lambda_, but it completely replaces the old population with the newly generated one.


### Creation of the Initial Population:

An initial game environment with a given dimension and population are created using the _create_game_and_population_ function.


### Results:

We chose to solve the problem with different configuration for problem dimension, population's parameters and probabilities. The maximum number of generation is fixed to 3000.
In the table below there are plots representing the results of the most important configuration on which we ran the problem.
The total fitness calls are printed at the end of the execution.

# SMALL - Problem Size = 1

(1+λ) always use ILM/DHC in dynamic configurations;
(1,λ) always use DHM/ILC in dynamic configurations
both always use MR = 0.2 and CR = 0.8 in static configurations

|   |  (1+λ) | (1+λ) rates |(1+λ) Results| (1,λ) | (1,λ) rates  |(1,λ) Results |
:-------------------------:|:-------------------------: |:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
| **mutateFlip, dynamic** | ![](DHMcmu1r.png) | |Fitness call = 60100 <br/> Fitness = 0.939 <br/> Generation level = 3000 | | | Fitness call = 167400 <br/> Fitness = 1.0 <br/> Generation level = 1670|
| **mutate, dynamic**|  ![]()| | Fitness call = 33500 <br/> Fitness = 1.0 <br/> Generation level = 1670| | |Fitness call = 8700 <br/> Fitness = 1.0 <br/> Generation level = 86 |
| **mutateFlip, static**| |![](outputs/output_Biotouch/18-15_02-02-2018/Verification/ITALIC/ITALIC_movementPoints_notbalanced_frrVSfpr.png)  | Fitness call = 60100 <br/> Fitness = 0.985 <br/> Generation level = 3000| | | Fitness call = 56600 <br/> Fitness = 1.0 <br/> Generation level = 565|
| **mutate, static**|  ![]()| |Fitness call = 37380 <br/> Fitness = 1.0 <br/> Generation level = 1864 | | |Fitness call = 56500 <br/> Fitness = 1.0 <br/> Generation level = 564 |

# BIG - Problem Size = 10

(1+λ) always use ILM/DHC in dynamic configurations;
(1,λ) always use DHM/ILC in dynamic configurations
both always use MR = 0.2 and CR = 0.8 in static configurations

|   |  (1+λ) | (1+λ) rates |(1+λ) Results| (1,λ) | (1,λ) rates  |(1,λ) Results |
:-------------------------:|:-------------------------: |:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|
| **mutateFlip, dynamic** | ![](DHMcmu1r.png) | |Fitness call = 60100 <br/> Fitness = 0.28 <br/> Generation level = 3000 | | | Fitness call = 178300 <br/> Fitness = 1.0 <br/> Generation level = 1782|
| **mutate, dynamic**|  ![]()| | Fitness call = 60100 <br/> Fitness = 0.62 <br/> Generation level = 3000| | |Fitness call = 7100 <br/> Fitness = 1.0 <br/> Generation level = 70 |
| **mutateFlip, static**| |![](outputs/output_Biotouch/18-15_02-02-2018/Verification/ITALIC/ITALIC_movementPoints_notbalanced_frrVSfpr.png)  | Fitness call = 60100 <br/> Fitness = 0.27 <br/> Generation level = 3000| | | Fitness call = 58100 <br/> Fitness = 1.0 <br/> Generation level = 580|
| **mutate, static**|  ![]()| |Fitness call = 60100 <br/> Fitness = 0.31 <br/> Generation level = 3000 | | |Fitness call = 53800 <br/> Fitness = 1.0 <br/> Generation level = 537 |

## Consideration

From the tables above we can see that both small and big problems can be solved with at least one configuration.
In particular we can observe that (1,λ) out-performs (1+λ) in terms of number of generation even if (1+λ) usually reach the objective with less fitness calls. 
In conclusion, in the problem with dimension = 10, (1+λ) doesn't often reach fitness = 1.0; instead (1,λ) seems to solve always the problem in all the configuration.

## Contribution
Made with the contribuition of Andrea Sillano s314771



