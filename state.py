from __init__ import *
from logic import GameLogic

class State():
    def __init__(self, matrix, active_index, playerManager):
        self.matrix = matrix
        self.active_index = active_index
        self.playerManager = playerManager
        self.big_matrix = np.ones((N))*empty_cell

    def get_valid_moves(self):
        self.check_small_boards()
        if(self.big_matrix[self.active_index]!=empty_cell):
            self.active_index = np.max(np.where(self.big_matrix==empty_cell))
        return np.where(self.matrix[self.active_index]==empty_cell)[0]

    def make_move(self, move):
        board = State(self.matrix.copy(), self.active_index, self.playerManager.copy())
        board.matrix[board.active_index][move] = board.playerManager.player.token_value
        board.active_index = move
        board.playerManager.change_player()
        return board

    def make_random_move(self):
        valid_moves = self.get_valid_moves()
        move = random.choice(valid_moves)
        return self.make_move(move)

    def check_small_boards(self):
        for index, small_board in enumerate(self.matrix):
            winner = GameLogic.get_winner(small_board)
            if(winner is not None):
                self.big_matrix[index] = winner

    def get_winner(self):
        self.check_small_boards()
        return GameLogic.get_winner(self.big_matrix)

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
