from __init__ import *

# Create a small Tic Tac Toe grid with pressable buttons
class TTTGrid(GridLayout):
    def __init__(self, **kwargs):
        super(TTTGrid, self).__init__(**kwargs)
        self.cols = 3
        self.matrix = np.ones(N)*empty_cell

        for i in range(N):
            box = Button(text=str(i), background_color=(0.9,0.9,0.9,0.25), color=(0,0,0,1), disabled=False, font_size=40)
            box.bind(on_press = self.press)
            self.add_widget(box)
        
    def render(self):
        for i, child in enumerate(self.children):
            if(self.matrix[i]!=empty_cell):
                child.disabled = True
                child.disabled_color = (0,0,0,1)

    def play(self, index):
        self.children[index].text = playerManager.player.token
        self.matrix[index] = playerManager.player.token_value

    def press(self, instance):
        index = self.children.index(instance)
        self.play(index)
        self.render()

        playerManager.change_player()
        self.parent.move_to(index)
        
        if(self.parent.AI_active==True and playerManager.player==playerManager.player_2):
            self.parent.AI_play()
        