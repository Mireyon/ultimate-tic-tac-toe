from __init__ import *
from uttt_grid import UTTTGrid

# Manages the layout of the game
class UTTT(App):
    def __init__(self, auto=None, score=[], **kwargs):
        super(UTTT, self).__init__(**kwargs)
        self.game = UTTTGrid()
        self.auto = auto
        self.score = score

    def on_start(self, **kwargs):
        if(self.auto is not None):
            self.root.children[0].children[0].children[0].trigger_action(duration=0.1)

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

        random_button = Button(text="Random", disabled=False)
        random_button.bind(on_press=self.automate)

        AI_button = ToggleButton(text='AI') 
        AI_button.bind(on_press=self.activateAI)

        match_button = ToggleButton(text='Versus')
        match_button.bind(on_press=self.matchAI)

        buttons_group = BoxLayout(orientation='horizontal', size_hint=(0.3,0.05))
        buttons_group.add_widget(random_button)
        buttons_group.add_widget(AI_button)
        buttons_group.add_widget(match_button)

        screen_layout.add_widget(buttons_group)
        root.add_widget(screen_layout)

        return root

    def restart(self, score):
        Clock.unschedule(self.game.auto_play)
        App.get_running_app().stop()
        self.score.append(score)
        new_app = UTTT(auto=True, score = self.score)
        new_app.run()

    # Work in progress
    def automate(self, instance):
        self.game.random_play()

    def activateAI(self, instance):
        if(instance.state=="down"):
            self.game.AI_active = True
        else:
            self.game.AI_active = False

    def matchAI(self, instance):
        if(instance.state=="down"):
            Clock.unschedule(self.game.auto_play)
            Clock.schedule_interval(self.game.auto_play, 0.1)
        else:
            Clock.unschedule(self.game.auto_play)
            print(f'There were {len(self.score)} matches and the player 1 won {self.score.count(-1)} times, the player 2 won {self.score.count(1)} times and there were {self.score.count(0)} draws')
