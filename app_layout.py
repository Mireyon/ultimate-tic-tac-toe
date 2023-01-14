from __init__ import *
from uttt_grid import UTTTGrid

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

    # Work in progress
    def automate(self, instance):
        self.game.random_play()

    def activateAI(self, instance):
        if(instance.state=="down"):
            self.game.AI_active = True
        else:
            self.game.AI_active = False
