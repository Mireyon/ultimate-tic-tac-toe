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
    def __init__(self, **kwargs):
        # super(State, self).__init__(**kwargs)
        self.last_move = None
        # self.last_moves = []
        self.starting_matrix = np.zeros((N,N))
        self.matrix = np.zeros((N,N))
        self.big_matrix = np.zeros(N)
        self.active_index = None

    def starting_state(self, current_matrix, big_matrix, active_index):
        self.starting_matrix = current_matrix.copy()
        self.starting_big_matrix = big_matrix.copy()
        self.starting_active_index = 8 - active_index

        self.matrix = current_matrix.copy()
        self.big_matrix = big_matrix.copy()
        self.active_index = 8 - active_index
        StatePlayer.token = Player.token
        StatePlayer.token_value = Player.token_value

    def update_matrix(self):
        list_playable_cells = []
        for i, matrix in enumerate(self.matrix):
            if(self.big_matrix[i]==0):
                matrix2D = matrix.reshape((3,3))
                diagonal = np.sum(np.diagonal(matrix2D))
                opposite_diagonal = np.sum(np.diagonal(np.fliplr(matrix2D)))
                lines = np.isin(np.sum(matrix2D, axis=1), three_values)
                columns = np.isin(np.sum(matrix2D, axis=0), three_values)
                cell_completed = np.all(matrix2D)
                if diagonal in three_values or opposite_diagonal in three_values or lines.any() or columns.any():
                    self.big_matrix[i] = StatePlayer.token_value

                elif cell_completed:
                    self.big_matrix[i] = 5

                else:
                    list_playable_cells.append(i)
        return list_playable_cells

    def get_valid_moves(self):
        # Update matrix and check if the active index corresponds to a playable cell
        list_playable_cells = self.update_matrix()
        if(len(list_playable_cells)==0):
            return []
        if(self.active_index not in list_playable_cells):
            self.active_index = np.min(list_playable_cells)
        small_cell_indexes = np.where(self.matrix[self.active_index]==0)[0]
        return small_cell_indexes

    def make_move(self, index):
        self.last_move = (self.active_index, index)
        new_state = State()
        new_state.starting_state(self.matrix, self.big_matrix, self.active_index)
        new_state.matrix[self.active_index][index] = StatePlayer.token_value
        new_state.last_move = self.last_move
        new_state.active_index = index
        StatePlayer.change_player()

        return new_state#self #Changer par State(blablabla) avec le new state

    def make_random_move(self, list_valid_indexes):
        index = random.choice(list_valid_indexes)
        return self.make_move(index)

    def reset(self):
        self.starting_state(self.starting_matrix, self.starting_big_matrix, 8 - self.starting_active_index)

    def get_winner(self):
        # self.last_move = self.last_moves[0]
        # print(f'Move is {self.last_move}')
        # self.last_moves = []
        matrix2D = self.big_matrix.reshape((3,3))

        diagonal = np.sum(np.diagonal(matrix2D))
        opposite_diagonal = np.sum(np.diagonal(np.fliplr(matrix2D)))
        lines = np.sum(matrix2D, axis=1)
        columns = np.sum(matrix2D, axis=0)

        # self.reset()
        if three_values[0]==diagonal or three_values[0]==opposite_diagonal or three_values[0] in lines or three_values[0] in columns:
            # print(f'Score : 1')
            return 1
        elif three_values[1]==diagonal or three_values[1]==opposite_diagonal or three_values[1] in lines or three_values[1] in columns:
            # print(f'Score : -1')
            return -1
        else:
            # print(f'Score : 0')
            return 0

    def display(self):
        print(f'\n{np.array(self.matrix)}')

class StatePlayer:
    token = "X"
    token_value = 1

    @staticmethod
    def change_player():
        if(StatePlayer.token=="X"):
            StatePlayer.token = "O"
            StatePlayer.token_value = 7
        else:
            StatePlayer.token = "X"
            StatePlayer.token_value = 1

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
        self.current_state = State()

        for _ in range(N):
            small_grid = TTTGrid()
            self.add_widget(small_grid)

        self.tree = MCTS(self.current_state)
    
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
        # self.update_complete_matrix()
        # self.current_state.display()

    def update_complete_cells(self):
        self.matrix[8-self.active_index] = mark_full
    
    def get_complete_matrix(self):
        matrix = []
        for tttgrid in self.children:
            matrix.insert(0, tttgrid.matrix.copy())
        return np.array(matrix)

    def AI_play(self, auto = False):

        current_matrix = self.get_complete_matrix()
        self.current_state.starting_state(current_matrix, self.matrix, self.active_index)
        tree = MCTS(self.current_state)
        tree.search(10)
        active_index, index = tree.best_move()
        # print(active_index, index)
        # button = self.children[8 - active_index].children[8 - index]
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