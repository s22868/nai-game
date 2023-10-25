from easyAI import TwoPlayerGame, Negamax, Human_Player, AI_Player
# import random

"""
Rules and instructions: README.md
Autorzy: Mateusz Budzyński, Igor Gutowski
Instructions for preparing the environment: README.md
"""

class TurnBasedGame(TwoPlayerGame):
    """
    This is a turn-based game where players move a certain number of fields in each turn.
    The player who reaches the end first wins. If players are on the same field, the one who was there first restarts.

    Attributes:
        players (list): A list containing the players in the game.
        num_fields (int): The total number of fields in the game.
        players_position (list): Current positions of the players on the field.
        current_player (int): The current player's turn (1 or 2).

    Methods:
        possible_moves(): Get a list of possible moves for the current player.
        make_move(move): Update the player's position based on the move made.
        win(): Check if the current player has won the game.
        is_over(): Check if the game is over.
        scoring(): Assign a score to the current game state based on the quality of the move for the AI player.
        show(): Display the current state of the game.
    """

    def __init__(self, players=None):
        """
        Initialize the TurnBasedGame instance.

        Parameters:
            players (list): A list of players in the game.
        """
        
        self.players = players
        self.num_fields = 20 # Target, last field
        self.players_position = [0, 0]  # Starting player positions
        # self.players_position = [random.randint(1, 3), random.randint(1, 3)]  # Random player positions
        self.current_player = 1  # Player 1 starts


    def possible_moves(self):
        """
        Get a list of possible moves for the current player.

        Returns:
            list: List of possible moves.
        """
        return [1, 2,3]

    def make_move(self, move):
        """
        Update the player's position based on the move made.

        Parameters:
            move (int): The move made by the current player.
        """
        self.players_position[self.current_player - 1] += move

        # Check if players are on the same field
        if self.players_position[0] == self.players_position[1]:
            # Reset other player to the starting position
            self.players_position[self.current_player % 2] = 0

    def win(self):
        """
        Check if the current player has won the game.

        Returns:
            bool: True if the current player has won.
        """
        return self.players_position[self.current_player -1] >= self.num_fields

    def is_over(self):
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over.
        """
        return self.players_position[1] >= self.num_fields or self.players_position[0] >= self.num_fields

    def scoring(self):
        """
        Assign a score to the current game state based on the quality of the move for the AI player.

        Returns:
            int: The score indicating the quality of the move for the AI player.
                - Higher positive scores favor moves that are beneficial for the AI.
                - Lower negative scores indicate moves that are disadvantageous for the AI.
        """
        return 1 if self.win() else -1

    def show(self):
        """
        Display the current state of the game.
        """
        print(f'p1 position: {self.players_position[0] * "#"}> {self.players_position[0]}/{self.num_fields}')
        print(f'p2 position: {self.players_position[1] * "#"}> {self.players_position[1]}/{self.num_fields}')

ai = Negamax(12)  # The AI will think 12 moves in advance
game = TurnBasedGame([AI_Player(ai), Human_Player()])
history = game.play()