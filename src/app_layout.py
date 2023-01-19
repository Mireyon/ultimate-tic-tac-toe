from __init__ import *
from uttt_grid import UTTTGrid

Builder.load_file('widgets.kv')
Builder.load_file('screens.kv')
Builder.load_file('game.kv')

class ScreenManagement(ScreenManager):pass

class StartScreen(Screen):
    def randomLoopPlay(self):
        self.manager.get_screen('game').randomLoopPlay()
class PlayScreen(Screen):
    def updateDifficulty(self):
        self.manager.get_screen('game').noDifficulty()

class SettingsScreen(Screen):pass
class CreditsScreen(Screen):pass

class LevelDifficulty(Screen):
    difficulty = ""
    def updateDifficulty(self, difficulty):
        LevelDifficulty.difficulty = difficulty
        self.manager.get_screen('game').updateDifficulty(difficulty)

class GameScreen(Screen):
    template = "Difficulty "
    difficulty = StringProperty(template)
    def updateDifficulty(self, difficulty):
        self.difficulty = GameScreen.template + difficulty
        self.start_game(difficulty=difficulty)

    def noDifficulty(self):
        self.difficulty = "Player vs Player"
        self.start_game()

    def start_game(self, difficulty=""):
        game_layout = self.children[0].children[-1].children[0].children[0]
        game_layout.clear_widgets()
        game = UTTTGrid(difficulty=difficulty)
        game_layout.add_widget(game)

        display_layout = self.children[0].children[0]
        display_layout.clear_widgets()
        display_layout.add_widget(Label(text="Player 1: "+str(game.playerManager.player_1.token), font_size=15, font_name="Trebuchet", size_hint=(0.8,1), color=(0,0,0,1)))
        display_layout.add_widget(Label(text="Player 2: "+str(game.playerManager.player_2.token), font_size=15, font_name="Trebuchet", size_hint=(0.8,1), color=(0,0,0,1)))
        display_layout.add_widget(Label(text="Current Player: "+str(game.playerManager.player.token), font_size=15, font_name="Trebuchet", size_hint=(0.8,1), color=(0,0,0,1)))

    def randomLoopPlay(self):
        game_layout = self.children[0].children[-1].children[0].children[0]
        game_layout.clear_widgets()
        game_layout.add_widget(UTTTGrid(difficulty="loop"))
    

class UTTT(App):
    def __init__(self, auto_play=False, **kwargs):
        super(UTTT, self).__init__(**kwargs)
        self.icon = "../assets/icon.png"
        self.auto_play = auto_play

    def build(self):
        LabelBase.register(name='Trebuchet', fn_regular='../assets/fonts/Trebuchet.ttf')
        # Create the screen manager
        screenManager = ScreenManager()
        with screenManager.canvas.before:
            Color(252/255, 250/255, 249/255, 1)
            Rectangle(pos=(0,0), size=(width, height))
        screenManager.add_widget(StartScreen(name='start'))
        screenManager.add_widget(PlayScreen(name='play'))
        screenManager.add_widget(SettingsScreen(name='settings'))
        screenManager.add_widget(CreditsScreen(name='credits'))

        screenManager.add_widget(LevelDifficulty(name='levelDifficulty'))
        screenManager.add_widget(GameScreen(name='game'))

        return screenManager

    def restart(self):
        gameScreen = self.root.get_screen('game')
        gameScreen.randomLoopPlay()
