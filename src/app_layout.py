from __init__ import *
from uttt_grid import UTTTGrid

# Manages the layout of the game
class UTTT(App):
    def __init__(self, auto=None, random_active=True, **kwargs):
        super(UTTT, self).__init__(**kwargs)
        self.game = UTTTGrid()
        self.auto = auto
        self.random_active = random_active
        self.icon = "../assets/icon.png"

    def on_start(self, **kwargs):
        if(self.auto is not None):
            if(self.random_active):
                self.root.children[0].children[0].children[1].trigger_action(duration=0.1)
            else:
                self.root.children[0].children[0].children[0].trigger_action(duration=0.1)

    def game_layout(self):
        main_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        sub_layout = BoxLayout(orientation='vertical', size=(475,475), size_hint=(None, None))
        sub_layout.add_widget(self.game)
        background_layout = BoxLayout(orientation='vertical', size=(600,600), size_hint=(None, None))
        background_layout.add_widget(Image(source='../assets/background_grid.png'))
        main_layout.add_widget(background_layout)
        main_layout.add_widget(sub_layout)
        return main_layout

    def build(self):
        self.title = "The Ultimate Tic-Tac-Toe"
        root = FloatLayout()
        with root.canvas.before:
            Rectangle(pos=(0,0), size=(width, height))
        root.add_widget(self.screen_layout())
        return root

    def screen_layout(self):
        screen_layout = BoxLayout(orientation='vertical')
        title_layout = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=(1,0.1))
        title_layout.add_widget(Label(text=self.title, color=(0,0,0,1), font_size=30, bold = True))

        screen_layout.add_widget(title_layout)
        screen_layout.add_widget(self.game_layout())

        random_button = Button(text="Random move", disabled=False)
        random_button.bind(on_press=self.game.random_play)

        AI_button = ToggleButton(text='Player vs AI') 
        AI_button.bind(on_press=self.activateAI)

        match_button = ToggleButton(text='Random vs AI')
        match_button.bind(on_press=partial(self.matchAI))

        match_AI_button = ToggleButton(text='AI vs AI')
        match_AI_button.bind(on_press=partial(self.AIvsAI))

        buttons_group = BoxLayout(orientation='horizontal', size_hint=(0.6,0.05))
        buttons_group.add_widget(random_button)
        buttons_group.add_widget(AI_button)
        buttons_group.add_widget(match_button)
        buttons_group.add_widget(match_AI_button)

        screen_layout.add_widget(buttons_group)
        return screen_layout

    def restart(self):
        Clock.unschedule(self.game.auto_play)
        self.game = UTTTGrid()
        self.root.clear_widgets()
        screen_layout = self.screen_layout()
        self.root.add_widget(screen_layout)
        self.auto = True
        self.on_start()

    def activateAI(self, instance):
        if(instance.state=="down"):
            self.game.AI_active = True
            self.game.disable_all()
            self.game.AI_play()
        else:
            self.game.AI_active = False

    def AIvsAI(self, instance):
        self.random_active = False
        self.matchAI(instance)

    def matchAI(self, instance):
        if(instance.state=="down"):
            Clock.unschedule(self.game.auto_play)
            Clock.schedule_interval(self.game.auto_play, 0.1)
        else:
            Clock.unschedule(self.game.auto_play)
            print("Match stopped")