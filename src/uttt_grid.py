from __init__ import *
from ttt_grid import TTTGrid
from logic import GameLogic
from render import GameRender
from player import PlayerManager
from model import Data

# Create the UTTT grid with small TTTs
class UTTTGrid(GridLayout):
    def __init__(self, difficulty="", **kwargs):
        super(UTTTGrid, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 30
        self.difficulty = difficulty
        self.playerManager = PlayerManager(difficulty=difficulty)
        self.matrix = np.ones(N, dtype=np.int8)*empty_cell
        self.active_index = random.choice(np.where(self.matrix==empty_cell)[0])

        for _ in range(N):
            small_grid = TTTGrid()
            self.add_widget(small_grid)
        
        if(self.difficulty=="loop"):
            Clock.schedule_interval(self.loop, 0)
        else:
            self.play()

    def loop(self, dt):
        if(self.disabled):
            Clock.unschedule(self.loop)
            App.get_running_app().restart()
            # App.get_running_app().stop()
            return
        self.playerManager.player.move(self)

    def play(self):
        if(self.disabled):
            App.get_running_app().stop()
            return
        if(self.playerManager.player==self.playerManager.player_2):
            if(self.difficulty==""):
                return 0
            else:
                self.disable_all()
                thread = Thread(target=self.playerManager.player.move, args=(self,))
                thread.daemon = True
                thread.start()

    def disable_all(self):
        for box in self.children:
            for button in box.children:
                button.disabled = True

    def is_end(self):
        big_winner = GameLogic.get_winner(self.matrix, self.playerManager)
        if(big_winner is not None):
            # Data.value = big_winner
            # self.update_data_nn()

            # self.update_csv(big_winner)
            self.disabled = True
            return True
        return False

    def update_data_nn(self):
        for state, policy in zip(Data.states, Data.pis):
            Data.write_csv(state, policy)

        Data.data.to_csv("../results/data.csv", sep=';', index=False)
        Data.clear()

    def update_csv(self, winner):
        if(winner==self.playerManager.player_1.token_value):
            output.loc['Player_1', 'win'] += 1
            output.loc['Player_2', 'loss'] += 1
        elif(winner==self.playerManager.player_2.token_value):
            output.loc['Player_2', 'win'] += 1
            output.loc['Player_1', 'loss'] += 1
        else:
            output.loc['Player_1', 'draw'] += 1
            output.loc['Player_2', 'draw'] += 1
        output.to_csv("../results/output.csv", sep=';')

    def get_index(self, index):
        if(self.matrix[index]!=empty_cell):
            index = np.max(np.where(self.matrix==empty_cell))
        return index

    #Only when a real player plays
    def enable_clickable_cells(self, index):
        self.disable_all()
        if(self.difficulty=="" or self.playerManager.player==self.playerManager.player_1):
            indexes = np.where(self.children[index].matrix==empty_cell)[0]
            for index in indexes:
                button = self.children[self.active_index].children[index]
                button.disabled = False

    def render(self):
        for child, cell in zip(self.children, self.matrix):
            if(cell!=empty_cell and not child.drawn):
                child.drawn = True
                GameRender.render_winner(child, cell, self.playerManager)

    def update_all(self):
        for index, child in enumerate(self.children):
            board = child.matrix
            winner = GameLogic.get_winner(board, self.playerManager)
            if(winner is not None):
                self.matrix[index] = winner
        self.render()

    def move_to(self, index):
        self.update_all()
        if(self.is_end()):return
        self.active_index = self.get_index(index)
        self.playerManager.switch_player()
        self.enable_clickable_cells(self.active_index)
        if(self.difficulty!="loop"): self.play()

    def get_copy(self):
        return np.array([tttgrid.matrix.copy() for tttgrid in self.children])
