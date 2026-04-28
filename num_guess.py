import random

class Player:
    def __init__(self):
        self.__best = None
        self.__games_played = 0
    
    def set_best(self, value):
        self.__best = value
    
    def get_best(self):
        return self.__best
    
    def increment_games_played(self):
        self.__games_played += 1
    
    def __str__(self):
        return f"Number of games played: {self.__games_played}\nBest game: {self.__best} attempts"

    __repr__ = __str__  


#TODO: Try to consolidate run_game function into the game class. Need to modify current functions.
class Game:
    def __init__(self):
        self.attempts = 0
        self.attempts_left = 7
        self.__chosen_num = random.randint(1, 100)

    def validate_input(self, string):
        try:
            output = int(string)
            return True
        
        except Exception:
            return False
    

    def update_player_stats(self, player, game_outcome):
        if game_outcome == "w" and ((player.get_best() == None) or (self.attempts < player.get_best())):
            player.set_best(self.attempts)
        
        player.increment_games_played()
    
    def make_guess(self, guess):
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
                self.update_player_stats(player, "w")
                end = True

            elif self.attempts_left == 0:
                print("\nOut of attempts! Better luck next time!")
                self.update_player_stats(player, "l")
                end = True

        #Display player stats after every game
        print("\nCurrent player stats:")
        print(player)
    
        
def start():
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
            repeat = False
        
        elif selection == "1":
            print("\nRepeat mode enabled. Starting new game...\n")
    return 


def main():
    start()
    return

if __name__ == "__main__":
    main()
