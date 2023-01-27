from src.imports import *
from src.uttt_grid import UTTTGrid

class Screen(Screen):
    language = StringProperty("English")
    current_language = "English"
    screen_list = [] 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__class__.screen_list.append(self)

    def changeLanguage(self):
        if(Screen.current_language == "English"):
            Screen.current_language = "Français"
        else:
            Screen.current_language = "English"

        for screen in Screen.screen_list:
            screen.language = Screen.current_language
            screen.property('language').dispatch(screen)

class ScreenManagement(ScreenManager): pass

class StartScreen(Screen):
    def randomLoopPlay(self):
        self.manager.get_screen('game').randomLoopPlay()
class PlayScreen(Screen):
    def updateDifficulty(self):
        self.manager.get_screen('game').noDifficulty()

class RulesScreen(Screen): 
    gif_path = os.path.join(src_path, "../assets/uttt.gif")

class SettingsScreen(Screen):
    list_music = os.listdir(src_path + "../assets/sounds/")
    music_index = 0
    current_music = StringProperty(list_music[music_index].rstrip(".mp3"))

    def changeMusic(self, value):
        if(self.music_index + value < 0 ):
            self.music_index = len(self.list_music) - 1
        elif(self.music_index + value >= len(self.list_music)):
            self.music_index = 0
        else:
            self.music_index += value
        self.current_music = self.list_music[self.music_index].rstrip(".mp3")
        isPlaying = App.get_running_app().background_music.state == "play"
        App.get_running_app().background_music.source = src_path + "../assets/sounds/" + self.list_music[self.music_index]
        if(isPlaying):
            self.playMusic()

    def manageMusic(self, value):
        self.playMusic() if(value) else self.stopMusic()

    def stopMusic(self):
        App.get_running_app().background_music.stop()

    def playMusic(self):
        App.get_running_app().background_music.play()

    def manageSound(self, value):
        App.get_running_app().background_music.volume = value

class LevelDifficulty(Screen):
    difficulty = ""
    def updateDifficulty(self, difficulty):
        LevelDifficulty.difficulty = difficulty
        self.manager.get_screen('game').updateDifficulty(difficulty)

class GameScreen(Screen):
    background_path = os.path.join(src_path, "../assets/background_grid.png")
    template = "Difficulty "
    difficulty = StringProperty(template)
    current_player = StringProperty("")

    def updateDifficulty(self, difficulty):
        if(self.language == 'English'):
            self.difficulty = GameScreen.template + difficulty
        else:
            if(difficulty == "easy"):
                self.difficulty = "Difficulté facile"
            elif(difficulty == "medium"):
                self.difficulty = "Difficulté moyenne"
            elif(difficulty == "hard"):
                self.difficulty = "Difficulté difficile"
            else:
                self.difficulty = "Difficulté impossible"

        self.start_game(difficulty=difficulty)

    def noDifficulty(self):
        self.difficulty = "Player vs Player" if(self.language == 'English') else "Joueur vs Joueur"
        self.start_game()

    @mainthread
    def updatePlayerTurn(self, playerManager):
        self.current_player = str(playerManager.player.token)
        player_turn_ui = self.ids.player_turn_ui
        with player_turn_ui.canvas.before:
            player_turn_ui.canvas.before.clear()
            Color(1,0,0,0.2) if(playerManager.player.token==playerManager.player_1.token) else Color(0,0,1,0.2)
            RoundedRectangle(pos=(player_turn_ui.pos[0]-5, player_turn_ui.pos[1]), size=(player_turn_ui.size[0]-10, player_turn_ui.size[1]), radius=[10,])

    def start_game(self, difficulty=""):
        winner_layout = self.ids.winner_layout
        winner_layout.clear_widgets()
        with winner_layout.canvas:
            winner_layout.canvas.clear()

        game_layout = self.ids.grid
        game_layout.clear_widgets()
        game = UTTTGrid(difficulty=difficulty)
        game_layout.add_widget(game)

        display_layout = self.ids.side_ui
        display_layout.clear_widgets()
        player1_text = "Player 1" if(self.language == 'English') else "Joueur 1"
        player2_text = "Player 2" if(self.language == 'English') else "Joueur 2"
        player1_text += ": "+str(game.playerManager.player_1.token)
        player2_text += ": "+str(game.playerManager.player_2.token)
        display_layout.add_widget(Label(text=player1_text, font_size=15, font_name="Trebuchet", size_hint=(0.8,1), color=(0,0,0,1)))
        display_layout.add_widget(Label(text=player2_text, font_size=15, font_name="Trebuchet", size_hint=(0.8,1), color=(0,0,0,1)))
        self.updatePlayerTurn(game.playerManager)

    def randomLoopPlay(self):
        winner_layout = self.ids.winner_layout
        winner_layout.clear_widgets()
        with winner_layout.canvas:
            winner_layout.canvas.clear()
        game_layout = self.ids.grid
        game_layout.clear_widgets()
        game_layout.add_widget(UTTTGrid(difficulty="loop"))

    @mainthread
    def start_IA_thinking(self):
        IA_layout = self.ids.ia_thinking
        thinking_text = "Thinking..." if(self.language == 'English') else "Réfléchit..."
        IA_layout.add_widget(Label(text=thinking_text, font_size=15, font_name="Trebuchet", size_hint=(0.8,1), pos_hint={'center_x':0.5, 'center_y':0.5}, color=(0,0,0,1)))
        IA_layout.add_widget(ProgressBar(max=100, value=0, size_hint=(0.8,0.8), pos_hint={'center_x':0.5, 'center_y':0.5}))
        # Clock.schedule_interval(self.IA_thinking, 0.1)

    @mainthread
    def IA_thinking(self, value):
        progress_bar = self.ids.ia_thinking.children[0]
        if(progress_bar.value!=value):
            progress_bar.value = value
            if(progress_bar.value >= 100):
                progress_bar.value = 0

    @mainthread
    def stop_IA_thinking(self):
        IA_layout = self.ids.ia_thinking
        # Clock.unschedule(self.IA_thinking)
        IA_layout.clear_widgets()

    @mainthread
    def show_winner(self, winner, playerManager):
        winner_layout = self.ids.winner_layout
        with winner_layout.canvas:
            if(winner==0):
                Color(1,1,0,0.4, mode="rgba")
            elif(winner==playerManager.player_1.token):
                Color(1,0,0,0.4, mode="rgba") 
            else:
                Color(0,0,1,0.4, mode="rgba")
            Rectangle(pos=winner_layout.pos, size=winner_layout.size)

        if(winner==0):
            winner_text = "Draw!" if(self.language == 'English') else "Egalité!"
        else:
            winner_text = "Player "+str(winner)+" wins!" if(self.language == 'English') else "Joueur "+str(winner)+" gagne!"
        winner_layout.add_widget(Label(text=winner_text, font_size=79, font_name="Trebuchet", size_hint=(0.8,1), pos_hint={'center_x':0.5, 'center_y':0.5}, color=(0,0,0,1)))
        winner_layout.add_widget(Label(text=winner_text, font_size=78, font_name="Trebuchet", size_hint=(0.8,1), pos_hint={'center_x':0.5, 'center_y':0.5}, color=(1,1,1,1)))

class UTTT(App):
    def __init__(self, **kwargs):
        super(UTTT, self).__init__(**kwargs)
        self.icon = src_path + "../assets/icon.png"
        self.title = "Ultimate Tic Tac Toe"
        sounds_path = src_path + "../assets/sounds/"
        self.background_music = SoundLoader.load(os.path.join(sounds_path, os.listdir(sounds_path)[0]))
        self.background_music.volume = 0.3
        self.background_music.play()
        self.background_music.loop = True

    def build(self):
        LabelBase.register(name='Trebuchet', fn_regular = src_path + '../assets/fonts/Trebuchet.ttf')
        # Create the screen manager
        self.screenManager = ScreenManager()
        with self.screenManager.canvas.before:
            Color(252/255, 250/255, 249/255, 1)
            Rectangle(pos=(0,0), size=(width, height))
        self.screenManager.add_widget(StartScreen(name='start'))
        self.screenManager.add_widget(PlayScreen(name='play'))
        self.screenManager.add_widget(RulesScreen(name='rules'))
        self.screenManager.add_widget(SettingsScreen(name='settings'))

        self.screenManager.add_widget(LevelDifficulty(name='levelDifficulty'))
        self.screenManager.add_widget(GameScreen(name='game'))

        return self.screenManager

    def restart(self):
        gameScreen = self.root.get_screen('game')
        gameScreen.randomLoopPlay()
