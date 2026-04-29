import random

class Player:
    """
        Represents a player across multiple rounds of the guessing game. Tracks the player's
        total games played and their best score (fewest attempts in a winning game).

        Attributes:
            __best [int or None]: The fewest attempts the player has won a game in. None if no game has been won yet.
            __games_played [int]: The total number of games the player has completed.
            __history [list]: A list containing the correct answer and number of attempts for each game the player has completed.
    """

    def __init__(self):
        self.__best = None
        self.__games_played = 0
        self.__history = []
    
    def set_best(self, value):
        """
            Sets the player's best score (fewest attempts) to the given value.

            Inputs:
                value [int]: The number of attempts to record as the player's best game.

            Outputs:
                None
        """
        self.__best = value
    
    def get_best(self):
        """
            Returns the player's current best score.

            Inputs:
                None

            Outputs:
                [int or None]: The fewest attempts the player has won a game in, or None if no game has been won yet.
        """
        return self.__best
    
    def get_games_played(self):
        return self.__games_played

    def increment_games_played(self):
        """
            Increments the player's total games played count by 1.

            Inputs:
                None

            Outputs:
                None
        """
        self.__games_played += 1

    def add_to_history(self, num, attempts, winloss):
        """
            Adds the results of a game to the player's history.

            Inputs:
                num [int]: The randomly generated number that is the solution to the game.
                attempts [int]: The number of attempts the player chose. 
                winloss [bool]: True if the game was won, false otherwise.
            
            Outputs:
                None
        """
        self.__history.append((num, attempts, winloss))
    
    def __str__(self):
        """
            Display's the player's gameplay statistics, including number of games played, personal best, and a table detailing the player's game history.

            Inputs:
                None

            Outputs:
                None
        """
        best = f"Personal best: {self.__best} attempts"

        if self.__best == None:
            best = "Personal best: N/A"

        num_games = f"\nNumber of games played: {self.__games_played}"
        player_history = f""

        #Build game history, each new line is a new game               
        for i in range(len(self.__history)):
            game = self.__history[i]
            answer = f"Answer was {game[0]}"
            attempts = f", Solved in {game[1]} attempts"

            win = game[2]
            if win == False:
                attempts = f", Loss"
            
            player_history = player_history + f"\nGame {i+1}: " + answer + attempts
        
        return best + num_games + player_history

    __repr__ = __str__  


class Game:
    """
        Represents a single round of the guessing game. Manages the randomly chosen target number,
        tracks the number of attempts made, and handles the core game logic for one round.

        Attributes:
            attempts [int]: The number of guesses the player has made in the current round.
            attempts_left [int]: The number of guesses remaining before the game is lost. Starts at 7.
            __chosen_num [int]: The randomly selected target number between 1 and 100 (inclusive).
    """
    def __init__(self):
        self.attempts = 0
        self.attempts_left = 7
        self.__chosen_num = random.randint(1, 100)

    def validate_input(self, string):
        """
            Checks whether a given string can be converted to an integer.

            Inputs:
                string [str]: The string to validate.

            Outputs:
                [bool]: True if the string is convertible to an integer, False otherwise.
        """
        try:
            output = int(string)
            return True
        
        except Exception:
            return False
    

    def update_player_stats(self, player, game_outcome):
        """
            Updates the player's stats at the end of a game. Increments games played, and updates
            the player's best score if the current game was won in fewer attempts than the previous best.

            Inputs:
                player [Player]: The Player object whose stats are to be updated.
                game_outcome [True]: Either True (win) or False (loss). Best score is only updated on a win.

            Outputs:
                None
        """
        if game_outcome == True:
            player.add_to_history(self.__chosen_num, self.attempts, True)
            if (player.get_best() == None) or (self.attempts < player.get_best()):
                player.set_best(self.attempts)
        
        else:
            player.add_to_history(self.__chosen_num, self.attempts, False)
        
        player.increment_games_played()
        
    
    def make_guess(self, guess):
        """
            Processes a single guess, updating attempt counts and comparing the guess to the chosen number.

            Inputs:
                guess [str]: A string representation of the player's guessed integer.

            Outputs:
                [str]: "Correct!" if the guess matches the chosen number, "Too low" if the guess is
                    below it, or "Too high" if the guess is above it.
        """
        self.attempts += 1
        self.attempts_left -= 1
        guess = int(guess)
        if guess == self.__chosen_num:
            return "Correct!"
        
        elif guess < self.__chosen_num:
            return "Too low"
        
        else:
            return "Too high"
    
    def __str__(self):
        return f"Number of attempts: {self.attempts}\nAttempts left: {self.attempts_left}"

    __repr__ = __str__

    def run_game(self, player):
        """
            Runs a single round of the guessing game. Manages the inner game loop, handling input
            validation, guess processing, and end conditions (correct guess or attempts exhausted).
            Displays player stats at the end of each round.

            Inputs:
                player [Player]: The Player object participating in this round.

            Outputs:
                None
        """
        print("Hello! This is a number guessing game. The computer has randomly selected a number between 1 and 100 (inclusive). You have 7 attempts. Please type in your first guess.")
        end = False
        while not end:
            print(f"\n{self}")
            guess = input("Guess: ")

        
            #Validate input loop. Repeatedly asks player until input is valid (i.e. an integer)
            valid = self.validate_input(guess)
            while not valid:
                print("\nYour guess must be an integer. Please try again.")
                guess = input("Guess: ")
                valid = self.validate_input(guess)

            #Prints output from guess
            output = self.make_guess(guess)
            print(f"\n{output}")       

            #Terminates inner single-game loop if correct answer is reached
            if output == "Correct!":
                print("\nCongratulations!")
                self.update_player_stats(player, True)
                end = True

            elif self.attempts_left == 0:
                print("\nOut of attempts! Better luck next time!")
                self.update_player_stats(player, False)
                end = True

        #Display player stats after every game
        print("\nCurrent player stats:")
        print("Number of games played: " + str(player.get_games_played()))
        
        if player.get_best() == None:
            print("Personal best: N/A")
        else:
            print(f"Personal best: {player.get_best()}")
    
        
def start():
    """
        Entry point for the game. Instantiates a Player and manages the outer loop that allows
        the player to play multiple rounds. After each round, prompts the player to play again
        or quit, repeatedly asking until a valid choice (0 or 1) is entered.

        Inputs:
            None

        Outputs:
            None
    """
    #start game by instantiating player
    player = Player()
    
    #Outer game loop governing repeat games
    repeat = True
    while repeat:
        game_instance = Game()
    
        #Run one round of the guessing game
        game_instance.run_game(player)

        #Prompt player if they want to repeat
        print("\nType 1 to play again. Type 0 to end the game.")
        selection = input("Input: ")

        #If input is not an integer and is not 1 or 0, repeatedly ask the player to make another input until a valid one is made
        while selection not in ("0", "1"):
            print("\nPlease type 0 or 1 to make your decision. Try again.")
            selection = input("Input: ")
        
        if selection == "0":
            print("\nThanks for playing!")
            print("\n" + str(player))
            repeat = False
        
        elif selection == "1":
            print("\nRepeat mode enabled. Starting new game...\n")
    return 


def main():
    start()
    return

if __name__ == "__main__":
    main()
