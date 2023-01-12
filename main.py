import random
import numpy as np
from monte_carlo_tree_search import Node, MCTS

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image

from kivy.config import Config
from kivy.graphics import Line, Color, Rectangle

# Global variables
N = 9                           # Tic Tac Toe size of 3x3
mark_full = 5                   # If matrix full
three_values = [3, 21]          # Triple 1 or triple 7
width = 800
height = 700

# Window configuration
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'height', height)
Config.set('graphics', 'width', width)

class State():
    def __init__(self, matrix, active_index, player):
        self.matrix = matrix
        self.active_index = active_index
        self.player = player

    def get_valid_moves(self):
        return np.where(self.matrix[self.active_index]==0)[0]

    def make_move(self, move):
        new_player = StatePlayer(self.player)
        board = State(self.matrix.copy(), self.active_index, new_player)
        board.matrix[board.active_index][move] = board.player.token_value
        board.active_index = move
        board.player.change_player()
        return board

    def make_random_move(self):
        valid_moves = self.get_valid_moves()
        if(len(valid_moves)==0):
            print(self.active_index)
            print(valid_moves)
        move = random.choice(valid_moves)
        return self.make_move(move)

    # A implémenter pour l'UTTT
    def get_winner(self):
        matrix2D = self.matrix[self.active_index].reshape((3,3))
        
        diagonal = np.sum(np.diagonal(matrix2D))
        opposite_diagonal = np.sum(np.diagonal(np.fliplr(matrix2D)))
        lines = np.sum(matrix2D, axis=1)
        columns = np.sum(matrix2D, axis=0)

        if three_values[0]==diagonal or three_values[0]==opposite_diagonal or three_values[0] in lines or three_values[0] in columns:
            return 1
        elif three_values[1]==diagonal or three_values[1]==opposite_diagonal or three_values[1] in lines or three_values[1] in columns:
            return -1
        elif(not np.any(self.matrix==0)):
            return 0
        else:
            return None

    def is_terminal(self):
        return self.get_winner() is not None

    def __str__(self) -> str:
        board = ''
        for i in range(3):
            for grid in self.matrix[i*3:i*3+3]:
                board += np.array2string(grid[:3]) + ' '

            board += '\n'
            for grid in self.matrix[i*3:i*3+3]:
                board += np.array2string(grid[3:6]) + ' '

            board += '\n'
            for grid in self.matrix[i*3:i*3+3]:
                board += np.array2string(grid[6:9]) + ' '

            board += '\n\n'
        
        return board


class StatePlayer:
    def __init__(self, player=None):
        self.token = "X"
        self.token_value = 1
        if(player is not None):
            self.token = player.token
            self.token_value = player.token_value

    def change_player(self):
        if(self.token=="X"):
            self.token = "O"
            self.token_value = 7
        else:
            self.token = "X"
            self.token_value = 1

# Manages the actual player
class Player:
    token = "X"
    token_value = 1

    @staticmethod
    def change_player():
        if(Player.token=="X"):
            Player.token = "O"
            Player.token_value = 7
        else:
            Player.token = "X"
            Player.token_value = 1

# Draw the lines when a cell is complete (todo : draw big O and big X)
class GameRender:
    @staticmethod
    def draw_lines(instance, i, j, width):
        M = instance.children
        with instance.canvas:
            Color(0,0,0,1, mode="rgba")
            Line(points=(M[i].center_x, M[i].center_y, M[j].center_x, M[j].center_y), width=width)

# Manages the core of the game
class GameLogic:
    @staticmethod
    def check_win(instance):
        matrix2D = instance.matrix.reshape((3,3))

        diagonal = np.sum(np.diagonal(matrix2D))
        opposite_diagonal = np.sum(np.diagonal(np.fliplr(matrix2D)))
        lines = np.isin(np.sum(matrix2D, axis=1), three_values)
        columns = np.isin(np.sum(matrix2D, axis=0), three_values)
        cell_completed = np.all(matrix2D)

        width = 3 if(isinstance(instance, TTTGrid)) else 8
        if diagonal in three_values:
            GameRender.draw_lines(instance, 0, 8, width)
            GameLogic.process_complete_cells(instance, cell_completed)

        elif opposite_diagonal in three_values:
            GameRender.draw_lines(instance, 2, 6, width)
            GameLogic.process_complete_cells(instance, cell_completed)

        elif lines.any():
            k = abs(2-np.where(lines)[0][0])
            GameRender.draw_lines(instance, k*3, k*3+2, width)
            GameLogic.process_complete_cells(instance, cell_completed)

        elif columns.any():
            k = abs(2-np.where(columns)[0][0])
            GameRender.draw_lines(instance, k, k+6, width)
            GameLogic.process_complete_cells(instance, cell_completed)

        elif cell_completed:
            GameLogic.process_complete_cells(instance, cell_completed)

    @staticmethod
    def process_complete_cells(instance, cell_completed):
        if(isinstance(instance, TTTGrid) and not cell_completed):
            GameLogic.update_matrix(instance.parent, instance.parent.active_index)
        elif(isinstance(instance, TTTGrid) and cell_completed):
            instance.parent.update_complete_cells()

    @staticmethod
    def update_matrix(instance, index):
        instance.matrix[8-index] = Player.token_value
        GameLogic.check_win(instance)

# Create a small Tic Tac Toe grid with pressable buttons
class TTTGrid(GridLayout):
    def __init__(self, **kwargs):
        super(TTTGrid, self).__init__(**kwargs)
        self.cols = 3
        self.matrix = np.zeros(N)

        for _ in range(N):
            box = Button(text="", background_color=(0.9,0.9,0.9,0.25), color=(0,0,0,1), disabled=False, font_size=40)
            box.bind(on_press = self.press)
            self.add_widget(box)
    
    def update_cell(self, instance):
        instance.disabled = True
        instance.disabled_color = (0,0,0,1)
        instance.text = Player.token

    def update_cell_matrix(self, instance):
        index = self.children.index(instance)
        GameLogic.update_matrix(self, index)
        self.parent.change_box(index)

    def press(self, instance):
        Player.change_player()
        self.update_cell(instance)
        self.update_cell_matrix(instance)

        if(self.parent.AI_active==True and Player.token=='O'):
            self.parent.AI_play()

# Create the UTTT grid with small TTTs
class UTTTGrid(GridLayout):
    def __init__(self, **kwargs):
        super(UTTTGrid, self).__init__(**kwargs)
        self.cols = 3
        self.spacing = 30
        self.matrix = np.zeros(N)
        self.active_index = 8
        self.AI_active = False

        for _ in range(N):
            small_grid = TTTGrid()
            self.add_widget(small_grid)
    
    def change_box(self, i):
        # Disable all buttons
        for box in self.children:
            for button in box.children:
                button.disabled = True

        # If grid is full, take first box starting from top left
        if(self.matrix[8-i]!=0):
            if((self.matrix==0).any()==False):
                self.disabled = True
                return   
            tmp = np.min(np.where(self.matrix==0))
            i = 8 - tmp

        # Make empty boxes clickable
        for active_button in self.children[i].children:
            if(active_button.text==""):
                active_button.disabled = False

        self.active_index = i

    def update_complete_cells(self):
        self.matrix[8-self.active_index] = mark_full
    
    def get_complete_matrix(self):
        matrix = []
        for tttgrid in self.children:
            matrix.insert(0, tttgrid.matrix.copy())
        return np.array(matrix)

    def AI_play(self, auto = False):
        player = StatePlayer()
        current_matrix = self.get_complete_matrix()
        self.current_state = State(current_matrix, 8 - self.active_index, player)
        tree = MCTS()
        new_board = tree.search(self.current_state, 1000)
        print(new_board)
        # index = np.where((current_matrix-new_board.state.matrix)!=0)[1][0]
        # button = self.children[self.active_index].children[8 - index]
        # button.trigger_action(0.1)

# Manages the layout of the game
class UTTT(App):
    def __init__(self, **kwargs):
        super(UTTT, self).__init__(**kwargs)
        self.game = UTTTGrid()

    def game_layout(self):
        main_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        sub_layout = BoxLayout(orientation='vertical', size=(475,475), size_hint=(None, None))
        sub_layout.add_widget(self.game)
        background_layout = BoxLayout(orientation='vertical', size=(600,600), size_hint=(None, None))
        background_layout.add_widget(Image(source='src/background_grid.png'))
        main_layout.add_widget(background_layout)
        main_layout.add_widget(sub_layout)
        return main_layout

    def build(self):
        self.title = "The Ultimate Tic-Tac-Toe"
        root = FloatLayout()
        with root.canvas.before:
            Rectangle(pos=(0,0), size=(width, height))
        screen_layout = BoxLayout(orientation='vertical')
        title_layout = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=(1,0.1))
        title_layout.add_widget(Label(text=self.title, color=(0,0,0,1), font_size=30, bold = True))

        screen_layout.add_widget(title_layout)
        screen_layout.add_widget(self.game_layout())

        automate_button = Button(text="Auto", disabled=False)
        automate_button.bind(on_press=self.automate)

        AI_button = ToggleButton(text='AI') 
        AI_button.bind(on_press=self.activateAI)

        buttons_group = BoxLayout(orientation='horizontal', size_hint=(0.1,0.05))
        buttons_group.add_widget(automate_button)
        buttons_group.add_widget(AI_button)

        screen_layout.add_widget(buttons_group)
        root.add_widget(screen_layout)

        return root

    def automate(self, instance):
        self.game.AI_play(True)

    def activateAI(self, instance):
        if(instance.state=="down"):
            self.game.AI_active = True
        else:
            self.game.AI_active = False

if __name__ == '__main__':
    UTTT().run()