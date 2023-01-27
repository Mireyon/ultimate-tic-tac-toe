from src.imports import *
from src.ttt_grid import TTTGrid
from src.logic import GameLogic
from src.render import GameRender
from src.player import PlayerManager

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

    # Dev only
    def loop(self, dt):
        if(self.disabled):
            Clock.unschedule(self.loop)
            # App.get_running_app().restart()
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
            App.get_running_app().screenManager.get_screen("game").show_winner(big_winner, self.playerManager)
            self.disabled = True
            return True
        return False

    def get_index(self, index):
        if(self.matrix[index]!=empty_cell):
            index = np.max(np.where(self.matrix==empty_cell))
        return index

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
        if(self.is_end()): return
        self.active_index = self.get_index(index)
        self.playerManager.switch_player()
        App.get_running_app().screenManager.get_screen("game").updatePlayerTurn(self.playerManager)
        self.enable_clickable_cells(self.active_index)
        if(self.difficulty!="loop"): self.play()

    def get_copy(self):
        return np.array([tttgrid.matrix.copy() for tttgrid in self.children])