import random
from game import Game, Move, Player
import esAgent
import rlAgent
import minMaxAgent
from tqdm import tqdm
import threading
import tableState


NUMBER_OF_PLAYS = 100

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

def playWithTrainedAgent():
    playerRL = rlAgent.RLPlayer()
    
    playerES = esAgent.EsPlayer()
    playerRL.loadPolicy("policy", "")
    playerES.loadPolicy("policyES")
    playerRandom = RandomPlayer()
    minMaxAg = minMaxAgent.minMaxPlayer()

    count = 0
    for _ in tqdm(range(NUMBER_OF_PLAYS)):
        g = Game()
        winner = g.play(minMaxAg,playerRL)
        
        if winner == 0:
            count += 1

    print(f"Winning Rate: {count*100/NUMBER_OF_PLAYS}%")


    
if __name__ == '__main__':
    
    playerRL = rlAgent.RLPlayer()
    playerRL.training()
    playerRL.play_for_statistics()
    
    
    playerES = esAgent.EsPlayer()
    playerES.training()
    playerES.play_for_statistics()

    playWithTrainedAgent()

    

