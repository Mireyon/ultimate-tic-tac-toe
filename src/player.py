from monte_carlo_tree_search import MCTS
from state import State
from model import Data
from __init__ import *

class Player(ABC):
    def __init__(self, token=None):
        self.token = token if(token is not None) else "X"
        self.token_value = 1 if(token=="X") else -1
    @abstractmethod
    def move(self):
        pass
    @abstractmethod
    def copy(self):
        pass

class HumanPlayer(Player):
    def __init__(self, token=None):
        super().__init__(token)
    def move(self):
        pass
    def copy(self):
        return HumanPlayer(self.token)

class RandomPlayer(Player):
    def __init__(self, token=None):
        super().__init__(token)
    def move(self, instance):
        index = random.choice(np.where(instance.children[instance.active_index].matrix==empty_cell)[0])
        button = instance.children[instance.active_index].children[index]
        button.trigger_action(0)
    def copy(self):
        return RandomPlayer(self.token)

class MctsPlayer(Player):
    def __init__(self, token=None):
        super().__init__(token)
    def move(self, instance):
        new_playerManager = instance.playerManager.copy()
        current_matrix = instance.get_copy()
        current_state = State(current_matrix, instance.active_index, new_playerManager, instance.matrix.copy())
        tree = MCTS()
        iterations = 500 if(instance.difficulty=="medium") else 1000
        new_board = tree.search(current_state, iterations)
        
        Data.add(current_matrix, tree.get_policy(tree.root))

        index = np.where((current_matrix-new_board.state.matrix)!=0)[1][0]
        button = instance.children[instance.active_index].children[index]
        button.trigger_action(0)

    def copy(self):
        return MctsPlayer(self.token)

class PlayerManager:
    def __init__(self, difficulty=""):
        self.difficulty = difficulty
        self.player_1 = HumanPlayer("X") if(difficulty!="loop") else MctsPlayer("X")
        self.player_2 = self.get_opposite_player()
        self.player = self.player_1 if(random.randint(0, 1)==0) else self.player_2

    def get_opposite_player(self):
        if(self.difficulty==""):
            return HumanPlayer("O")
        elif(self.difficulty=="easy"):
            return RandomPlayer("O")
        elif(self.difficulty=="medium" or self.difficulty=="hard"):
            return MctsPlayer("O")
        else:
            return MctsPlayer("O")

    def switch_player(self):
        self.player = self.player_2 if(self.player==self.player_1) else self.player_1
    
    def copy(self):
        playerManager = PlayerManager(self.difficulty)
        playerManager.player_1 = self.player_1.copy()
        playerManager.player_2 = self.player_2.copy()
        playerManager.player = playerManager.player_1 if(self.player==self.player_1) else playerManager.player_2
        return playerManager