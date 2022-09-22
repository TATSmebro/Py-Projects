import random
#unfinished negosyo

class Player():
    def __init__(self, score = 0, lifelines_used = 1, guesses = 10, curr_guess = 0):
        self.score = 0
        self.lifelines_used = 1
        self.guesses = 10
        self.curr_guess = 0

    def lifeline(type):
        if type == 'lifeline#1':
            self.guesses -= 1
        else:
            self.guesses -= 1

class Code():
    def __init__(self, len_code):
        self.val = []
        self.len = len_code

        for i in range(len_code):
            self.val.append(random.randint(0, 9))

def input_for_code_length():
    #Asks for user input for difficulty which corresponds to code length
    '''
    checks if the input is valid. Returns the player's input if it is valid. 
    If not, it repeats until the user inputs a valid difficulty.
    '''
    difficulty = {'Easy': 4, 'Medium': 5, 'Hard': 6, 'Extreme': 7, 'Impossible': 8}
    
    print('Type "end" anytime to end the game.')
    #Select difficulty prompt
    user_input = input('''
    Select Difficulty:
    "Easy" - 4
    "Medium" - 5
    "Hard" - 6
    "Extreme" - 7
    "Impossible" - 8
    Choose: ''')
    
    #Validates player input. Checks if player's input is allowed and asks for another input otherwise.
    while (user_input not in difficulty):
        
        if(user_input == "end"):
            restart()
        
        print("Invalid Input. Select from the choices")
        user_input = input('''
    Select Difficulty: 
    "Easy" - 4
    "Medium" - 5
    "Hard" - 6
    "Extreme" - 7
    "Impossible" - 8
    Choose: ''')

    return int(difficulty[user_input])

def input_for_guess(guess_num, code, total_guesses, lifeline_used):
    #Asks player to input a guess
    '''
    Checks if the guess made by the user is valid. If valid, it returns the player's guess. 
    If not, it repeats until the player inputs a valid guess.
    '''
    allowed = set("0123456789")

    print(f"Guess #{guess_num}")
    guess = input("Enter guess > ")
    
    #If player guesses
    while not(len(guess) == len(code) and allowed.issuperset(guess)):
        #If player ends game.
        if(guess == "end"):
            restart()
        #If player uses lifeline
        if(guess == "lifeline#1"):
            if (total_guesses-guess_num) > 1 and lifeline_used == 0:
                random_num_pos = random.randint(0, (len(code)-1))
                print(f"Hidden code contains digit {code[random_num_pos]}")
                return guess
        if(guess == "lifeline#2"):
            if (total_guesses-guess_num) > 2 and lifeline_used == 0:
                random_num_pos = random.randint(0, (len(code)-1))
                print(f"Hidden code contains digit {code[random_num_pos]} at position {random_num_pos+1}")
                return guess
        #If input is invalid
        print("Invalid guess or insufficient guesses/lifelines left.")
        print(f"Code is only of length {len(code)}\n")
        print(f"Guess #{guess_num}")
        guess = input("Enter guess > ")
    
    return guess

def compare_guess_to_code(code, guess_array):
    #Compares the player's guess to the hidden code. Returns the value of the "R" red code pegs.
    
    temp = [i for i in code] #Creates a temporary copy of the code.
    R = 0 #Red peg tracker
    W = 0 #White peg tracker

    #Check for Red Pegs (Same value and position)
    '''
    Replaces checked value  with '?' to avoid referencing one value more than once
    '''
    for i, num in enumerate(guess_array):
        if num == temp[i]:
            temp[i] = '?'
            guess_array[i] = '?'
            R += 1
    
    #Check for White Pegs (Same value, different position)
    '''
    Replaces checked value  with '?' to avoid referencing one value more than once
    '''
    for i, num in enumerate(guess_array):
        if num != '?' and num in temp:
            temp[temp.index(num)] = '?'
            guess_array[i] = '?'
            W += 1

    print(f"{R}R - {W}W\n")
    return R

def rules():
    print('''
        === Overview
    The objective of the game is for the user (henceforth referred to as the "codebreaker") 
    to figure out a pattern (henceforth referred to as the "code") with no more than 10 guesses.

        === Starting the Game
    1. The codebreaker shall first be asked to input difficulty which pertains to a code length.
        "Easy" - 4
        "Medium" - 5
        "Hard" - 6
        "Extreme" - 7
        "Impossible" - 8 
        This will be the length (n) of the pattern to be guessed.
    2. The CPU will then generate the code containing n digits.

        === Guesses
    Once the game has started, the codebreaker will be asked to `Enter a guess`. 
    Each guess must contain exactly n digits from 0-9. Codebreakers are also allowed to repeat the use of digits. 
    For example, if length (n) is 4. then `0123` or `0011` can be considered valid guesses. 
    The codebreaker is allowed a default of "10 guesses".

        === Lifelines
    Players can use lifelines (clues) in order to help them. typing "lifeline#1" will reveal a single value in the code.
    Typing "lifeline#2" will reveal a single value and its position within the code. Players can only use one lifeline 
    throughout the whole game.

        === Invalid Guess
    The program will check for invalid guesses. If a codebreaker submits an invalid guess, the program will ask for another input. 
    Invalid guesses "do not affect the total number of guesses".
    Inputs with unnecessary spaces also count as invalid guesses.
    For example, if length (n) is 4. then `12345`,  `1234`,`1234` ,`1 2 3 4`, and `1 234` would be considered as invalid guesses.

        === Key Pegs
    In the game, there are two (2) types of key pegs: red (R) and white (W). These may be used to help the codebreaker figure out the code.

        === Red Peg (R)
    A red peg indicates that the guess contains a digit which is found in the code and in the right position.

        === White Peg (W)
    A white peg indicates that the guess contains a digit found in the code but in the wrong position.

    For example, the code is `1234` and Guess #1 is `1432`, then the CPU will display `2R - 2W`, 
    indicating that there are 2 digits in the right position (in this case `1` and `3`), and 2 digits in the wrong position (`4` and `2`)
    ''')
    return game_menu()

def game_menu():
    #Main Menu
    options = {'Start': 'main()', 'Rules': 'rules()'}
    
    #Asks user for input
    inp = input('''
    ======MASTERMIND======

    --------Start---------
    --------Rules---------
    ---------end----------
    Choose: ''')

    #Incase of invalid input or if player exits the game.
    while inp not in options:
        if inp == 'end':
            print('Thank you for trying the program!')
            exit()
        
        print('Invalid input. Choose Again')
        inp = input('''
    ======MASTERMIND======

    --------Start---------
    --------Rules---------
    ---------end----------
    Choose: ''')

    exec(options[inp])

def restart():
    inp = input('Do you want to restart? ["Y" / "N"]: ')

    while inp not in ('Y', 'N'):
        print('Invalid input. Try Again.')
        inp = input('Do you want to restart? ["Y" / "N"]: ')

    if inp == 'Y':
        game_menu()
    else:
        print('Thank you for playing!')
        exit()

def main():
    #get input for code length
    code_length = input_for_code_length()
    print()
    print(f"Hidden code is of length {code_length}")
    print("Total number of Guesses: 10")

    #generates the code as an array based on code length
    code = Code(code_length)

    total_guesses = 10
    guess_num = 1
    lifeline_used = 0

    while guess_num <= total_guesses:
        guess = input_for_guess(guess_num, code, total_guesses, lifeline_used)

        if(guess == "lifeline#1"):
            total_guesses -= 1
            lifeline_used += 1
        elif(guess == "lifeline#2"):
            total_guesses -= 2
            lifeline_used += 1
        else:

            guess_array = [int(char) for char in guess]

            #player wins if the value of the red code pegs is equal to the code's length
            if(compare_guess_to_code(code, guess_array) == code_length):
                print("YOU WIN!!")
                restart()
            guess_num += 1
    
    print(f'YOU LOST!! The code was {code}')
    restart()


if __name__ == '__main__':
    game_menu()