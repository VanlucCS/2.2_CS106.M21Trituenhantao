"""Class containing Human vs AI functions have interface."""

from mcts import MonteCarloTreeSearch, TreeNode
from config import CFG
from tkinter import *
from matplotlib.pyplot import draw, grid
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'

class Tic_Tac_Toe_UI(object):
    """Class with functions for a Human vs an AI game have interface. 

    Attributes:
        game: An object containing the game state.
        net: An object containing the neural network.
    """
    
    def __init__(self,game,net):
        self.game = game
        self.game2 = self.game.clone()
        self.net = net
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)
        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0
        # Mcts
        self.mcts = MonteCarloTreeSearch(self.net)
        self.node = TreeNode()
    
    def get_action(self,game):
        """Function to get action for the AI use mcts."""
        
        best_child = self.mcts.search(self.game2, self.node,CFG.temp_final)
        action = best_child.action
        self.game2.play_action(action)
        best_child.parent = None
        self.node = best_child
        return action

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))
        self.node = TreeNode()
        self.game2=self.game.clone()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        #get action use mcts
        action = self.get_action(self.game2)
        action = [ (n*2+1)*100 for n in action]
        grid_position =[action[1],action[2]]

        logical_position = self.convert_grid_to_logical_position(grid_position)

        self.board_status[logical_position[1]][logical_position[0]] = 1
        self.canvas.create_oval(grid_position[1] - symbol_size, grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, grid_position[0] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        best_child = TreeNode()         

        action =[1,0,0]
        action[1] = int(((grid_position[1]/100) -1)/2)
        action[2] = int(((grid_position[0]/100) -1)/2)

        self.game2.play_action(action)
        best_child.action = action
        best_child.parent = None
        self.node = best_child

        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'You won!'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'You loseeee :(('
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Draw Match'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 30 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'YOU (X)    : ' + str(self.X_score) + '\n'
        score_text += 'AI (O)     : ' + str(self.O_score) + '\n'
        score_text += 'Draw Match : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

   

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('You won!')
        if self.O_wins:
            print('You loseee :((')
        if self.tie:
            print('Draw Match')

        return gameover

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        if not self.reset_board:  
            if not self.is_grid_occupied(logical_position):
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1

                if not self.is_gameover():    
                    # AI_turns
                    l_po =self.draw_O(logical_position)

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again on click
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

