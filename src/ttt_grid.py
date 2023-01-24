from __init__ import *

# Create a small Tic Tac Toe grid with pressable buttons
class TTTGrid(GridLayout):
    def __init__(self, **kwargs):
        super(TTTGrid, self).__init__(**kwargs)
        self.cols = 3
        self.matrix = np.ones(N, dtype=np.int8)*empty_cell
        self.drawn = False

        for _ in range(N):
            box = Button(text="", background_color=(0.9,0.9,0.9,0.25), color=(0,0,0,1), disabled=False, font_size=40, disabled_color=(0,0,0,1))
            box.bind(on_press = self.press)
            self.add_widget(box)

    def play(self, index):
        self.children[index].text = self.parent.playerManager.player.token
        self.matrix[index] = self.parent.playerManager.player.token_value

    def press(self, instance):
        index = self.children.index(instance)
        self.play(index)
        self.parent.move_to(index)

        