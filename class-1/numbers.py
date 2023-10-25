from easyAI import TwoPlayerGame, Negamax, Human_Player, AI_Player

"""
Rules and instructions: README.md
Autorzy: Mateusz Budzyński, Igor Gutowski
Instructions for preparing the environment: README.md
"""

class NumberRace(TwoPlayerGame):
    """A simple number race game where players take turns adding numbers and aim to reach a target number."""

    def __init__(self, players=None, target=100):
        """
        Initialize the NumberRace instance.

        Parameters:
            players (list): A list of players in the game.
            target (int): The target number the players aim to reach.
        """
        self.players = players
        self.target = target # Target number
        self.current_player = 1  # Player 1 starts
        self.current_number = 0  # Current number that players add to

    def possible_moves(self):
        """Get a list of possible moves for the current player."""
        return [i for i in range(1, 6)]  # Players can add numbers from 1 to 5

    def make_move(self, move):
        """Update the current number based on the move made by the current player."""
        self.current_number += move

    def win(self):
        """Check if the current player has won the game."""
        return self.current_number >= self.target  # Player wins if they reach or exceed the target

    def is_over(self):
        """Check if the game is over."""
        return self.win()  # Game stops when someone wins.

    def scoring(self):
        """
        Assign a score to the current game state based on the quality of the move for the AI player.

        Returns:
            int: The score indicating the quality of the move for the AI player.
                - Higher positive scores favor moves that are beneficial for the AI.
                - Lower negative scores indicate moves that are disadvantageous for the AI.
        """
        if self.win():
            return 100 if self.current_player == 1 else -100  # Assign score based on the winner
        return 0  # If the game is not over, return a neutral score

    def show(self):
        """Display the current state of the game."""
        print(f"{self.current_number * '*'}{(self.target - self.current_number) * ' '} {self.current_number} / {self.target}")

ai = Negamax(10)  # The AI will think 10 moves in advance
game = NumberRace([AI_Player(ai), Human_Player()], target=40)
history = game.play()