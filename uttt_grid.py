from __init__ import *
from ttt_grid import TTTGrid
from logic import GameLogic
from render import GameRender
from state import State
from monte_carlo_tree_search import MCTS

# Create the UTTT grid with small TTTs
class UTTTGrid(GridLayout):
    def __init__(self, **kwargs):
        super(UTTTGrid, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 30
        self.matrix = np.ones(N)*empty_cell
        self.active_index = 0
        self.AI_active = False

        for _ in range(N):
            small_grid = TTTGrid()
            self.add_widget(small_grid)

    def disable_all(self):
        for box in self.children:
            for button in box.children:
                button.disabled = True

    def get_index(self, index):
        big_winner = GameLogic.get_winner(self.matrix)
        if(big_winner is not None):
            print(f'Game is finished !')
            self.disabled = True
            return None

        if(self.matrix[index]!=empty_cell):
            index = np.max(np.where(self.matrix==empty_cell))
        return index

    def enable_clickable_cells(self, index):
        indexes = np.where(self.children[index].matrix==empty_cell)[0]
        for index in indexes:
            button = self.children[self.active_index].children[index]
            button.disabled = False

    def render(self):
        for child, cell in zip(self.children, self.matrix):
            if(cell!=empty_cell):
                GameRender.render_winner(child, cell)

    def update_all(self):
        for index, child in enumerate(self.children):
            board = child.matrix
            winner = GameLogic.get_winner(board)
            if(winner is not None):
                self.matrix[index] = winner

    def move_to(self, index):
        self.update_all()
        self.render()
        self.disable_all()
        index = self.get_index(index)
        if(index is None):
            return None
        self.active_index = index
        self.enable_clickable_cells(index)
    
    def random_play(self):
        if(self.disabled==False):
            index = random.choice(np.where(self.children[self.active_index].matrix==empty_cell)[0])
            button = self.children[self.active_index].children[index]
            button.trigger_action(0.1)
            time.sleep(0.1)

    def get_copy(self):
        # matrix = []
        # for tttgrid in self.children:
        #     matrix.insert(0, tttgrid.matrix.copy())
        # return np.array(matrix)
        return np.array([tttgrid.matrix.copy() for tttgrid in self.children])

    def AI_play(self):
        new_playerManager = playerManager.copy()
        current_matrix = self.get_copy()
        self.current_state = State(current_matrix, self.active_index, new_playerManager)
        tree = MCTS()
        new_board = tree.search(self.current_state, 5)
        index = np.where((current_matrix-new_board.state.matrix)!=0)[1][0]
        button = self.children[self.active_index].children[index]
        button.trigger_action(0.1)
