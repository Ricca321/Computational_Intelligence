import hashlib
import random
class Entry():
    def __init__(self):
       self.table_prob = []
       self.table_move_prob = []
       self._init_table_points()

    def edit_table_cell_prob(self, table_prob, table_move_prob):
        if table_prob == None or table_move_prob==None:
            self._init_table_points()
        else:
            self.table_prob = table_prob
            self.table_move_prob = table_move_prob
       
    def get_table_cell_prob(self):
        return self.table_prob
    
    def get_table_move_prob(self):
        return self.table_move_prob
    
    def get_entry_c(self):
        return (self.get_table_cell_prob(), self.get_table_move_prob())
    
    def _init_table_points(self):
        self.table_prob = [[0 for _ in range(5)] for _ in range(5)]
        self.table_move_prob = [[[0 for _ in range(4)] for _ in range(5)] for _ in range(5)]
        for i in range(5):
            self.table_prob[0][i] = 0.1
            self.table_prob[4][i] =  0.1
            self.table_prob[i][0] =  0.1
            self.table_prob[i][4] =  0.1

       
        self.table_move_prob[0][0] = [0,0.1,0,0.1]
        self.table_move_prob[0][4] = [0,0.1,0.1,0]
        self.table_move_prob[4][0] = [0.1,0,0,0.1]
        self.table_move_prob[4][4] = [0.1,0,0.1,0]
        for i in range(1,4):
                    self.table_move_prob[0][i] = [0, 0.1, 0.1, 0.1]
                    self.table_move_prob[4][i] = [0.1,0, 0.1, 0.1]
                    self.table_move_prob[i][0] = [ 0.1, 0.1,0,0.1]
                    self.table_move_prob[i][4] = [ 0.1,0.1,0.1,0]

class TableState():
    def __init__(self):
        self.table_state = {}
        
    def add_or_modify_state(self, state , table_cell_prob, table_move_prob):
        hashed_state = self.hash_state(state) 
        entry = Entry()
        entry.edit_table_cell_prob(table_cell_prob, table_move_prob)
        self.table_state[hashed_state] = entry

    def get_state(self, state: str):
        hashed_state = self.hash_state(state) 
        if self.table_state.get(hashed_state)!=None:
            entry = self.table_state.get(hashed_state)
            return entry.get_entry_c()
        else:  
            return False
        
    def get_state_len(self):
        return len(self.table_state)


    def hash_state(self, state: str)->str:
        return hashlib.sha256(str(state).encode()).hexdigest()
    
    def print_table(self):
        
        for k, e in  enumerate(self.table_state):
            if k == 1:
                break
            entry = self.table_state[e].get_entry_c()
            for i in range(0, len(entry[0])):
                for j  in range(0, len(entry[0][i])):
                    print("[","%.2f" % round(entry[0][i][j], 2),"] ", end='')
                print("")
