import random

def check_input_length():
    #checks if the inputted number is between 4 to 8. Returns the player's input if it is valid. If not, it repeats until the user inputs a valid number.
    print("Type \"end\" at anytime to end the game.")
    user_input = input("Input a number between 4 to 8 to determine the length of the code: ")
    if(user_input == "end"):
        exit()
    
    #the .issuperset() function returns true if all values in "user_input" are also in "allowed"
    allowed = set("0123456789")
    if(allowed.issuperset(user_input) and int(user_input) >= 4 and int(user_input) <= 8):
        return int(user_input)
    else:
        print("Invalid code length.")
        print("Code can only be from 4 to 8 digits long.")
        print()
        return check_input_length()

def check_guess_validity(guess_num, code):
    #checks if the guess made by the user is valid. If valid, it returns the player's guess. If not, it repeats until the player inputs a valid guess.
    print(f"Guess #{guess_num}")
    guess = input("Enter guess > ")
    
    if(guess == "end"):
        exit()
    elif(guess == "lifeline#1"):
        random_num = random.randint(0, (len(code)-1))
        print("Hidden code contains digit", code[random_num])
        return guess
    elif(guess == "lifeline#2"):
        random_num = random.randint(0, (len(code)-1))
        print("Hidden code contains digit", code[random_num], "at position", random_num+1)
        return guess

    
    allowed = set("0123456789")
    if(len(guess) == len(code) and allowed.issuperset(guess)):
        return guess
    else:
        print("Invalid Guess.")
        print("Code is only of length", len(code))
        print()
        return check_guess_validity(guess_num, code)

def compare_guess_to_code(code, guess_array):
    #Compares the player's guess to the hidden code. Returns the value of the "R" red code pegs.
    
    R = 0
    W = 0 
    W_found = []
    temp_code = [i for i in code]
    for i in range(len(code)):
        for j in range(len(guess_array)):
            if(temp_code[i] == guess_array[i]):
                R+=1
                W_found.append(temp_code[i])
                #sets the digit in temp_code[i] to "?" so that R will not get increased when there are duplicates.
                temp_code[i] = "?"
            elif(temp_code[i] == guess_array[j]):
                #---------not sure how to properly check for duplicates when it comes to the white code pegs.----------
                if(temp_code[i] in W_found or temp_code[i] == "?"):
                    break
                else:
                    W+=1
                    W_found.append(temp_code[i])

    # print("Temp Code:   ", temp_code)
    # print("W_found:     ", W_found)
    print(f"{R}R - {W}W")
    print()
    return R

#get input for code length
code_length = check_input_length()
print()
print("Hidden code is of length", code_length)
print("Total number of Guesses: 10")

#generates the code as an array based on code length
code = [random.randint(0,9) for i in range(code_length)]


#prints hidden code
# print("code is: ", end='')
# for i in code:
#     print(i,end='')
# print()

total_guesses = 10
guess_num = 1
while guess_num <= total_guesses:
    guess = check_guess_validity(guess_num, code)

    if(guess == "lifeline#1"):
        total_guesses -= 1
    elif(guess == "lifeline#2"):
        total_guesses -= 2
    else:

        guess_array = [int(char) for char in guess]

        #show the arrays of the hidden code and the player's guess
        # print("Hidden Code: ",code)
        # print("Guess:       ", guess_array)

        if(compare_guess_to_code(code, guess_array) == code_length):
            print("YOU WIN!!")
            exit()
        guess_num += 1




    #player wins if the value of the red code pegs is equal to the code's length



    


