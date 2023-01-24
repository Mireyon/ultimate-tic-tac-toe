from src.imports import *
# Manages the core of the game
class GameLogic:
    @staticmethod
    def get_winner(matrix, playerManager):
        matrix2D = matrix.reshape((3,3))

        diagonal = np.sum(np.diagonal(matrix2D))
        opposite_diagonal = np.sum(np.diagonal(np.fliplr(matrix2D)))
        lines = np.sum(matrix2D, axis=1)
        columns = np.sum(matrix2D, axis=0)

        if three_values[0]==diagonal or three_values[0]==opposite_diagonal or three_values[0] in lines or three_values[0] in columns:
            return playerManager.player_2.token_value
        elif three_values[1]==diagonal or three_values[1]==opposite_diagonal or three_values[1] in lines or three_values[1] in columns:
            return playerManager.player_1.token_value
        elif(not np.any(matrix2D==empty_cell)):
            return 0
        else:
            return None