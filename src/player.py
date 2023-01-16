# Manages the actual player
class Player:
    def __init__(self, token=None):
        self.token = token if(token is not None) else "X"
        self.token_value = 1 if(token=="X") else -1

class PlayerManager:
    def __init__(self):
        self.player_1 = Player("X")
        self.player_2 = Player("O")
        self.player = self.player_1

    def change_player(self):
        if(self.player.token=="X"):
            self.player = self.player_2
        else:
            self.player = self.player_1
    
    def copy(self):
        playerManager = PlayerManager()
        playerManager.player_1 = Player(self.player_1.token)
        playerManager.player_2 = Player(self.player_2.token)
        playerManager.player = playerManager.player_1 if(self.player.token=="X") else playerManager.player_2
        return playerManager