from random import choice, randint

def input_valid_str(question, errortext, possible_answers):
    answer = input(question)
    # While user answer is not valid
    while answer not in possible_answers:
        print(errortext)
        answer = input(question)
    return answer

def input_valid_int(question, errortext, min, max):
    while True: # Loop until correct input
        str_input = input(question)
        if str_input.isdigit(): # Only containing digits (0-9)
            answer = int(str_input)
            if min <= answer <= max:
                return answer # Correct choice, return value
            else:
                print(errortext)
        else:
            print(errortext)

def input_valid_math_answer(question, errortext):
    while True: # Loop until correct input
        str_input = input(question)
        if str_input.isdigit(): # Only containing digits (0-9)
            answer = int(str_input)
            return answer # returned if answer is digit
        else:
            print(errortext)

# Called at the beginning of the game and when restarting after losing
def input_play_game(question, n_message, y_message):
    answer = input_valid_str(question, 'Choose \'y\' for yes and \'n\' for no', ('y', 'n'))
    if answer == 'n':
        print(n_message)
        return False
    elif answer == 'y':
        print(y_message)
        return True

# Printed out when door does not lead to the zombies
# I chose to use print also in a method as otherwise it
# would have been repeated several times in the main program
def print_good_door(zombie_door, answered_questions, doors_left):
    print('\nPhew, no zombies in sight!')
    print(f'They were hiding behind door {zombie_door}')
    print(f'You have now made it through question {answered_questions}.')
    print(f'{doors_left} questions and {doors_left} doors to go.')
    print('You get a new question.\n')
    return True

# Method generating random values to the 'r'-option
def generate_new_values(doors_left):
    zombie_door = randint(1, doors_left)
    factor_or_dividend = randint(0, 12)
    return zombie_door, factor_or_dividend

# Method used when calculation_methos is not 'r'
# I chose to put input in a method to make a less messy main and to avoid repetition
def calculate(table_or_divisor, factor_or_dividend, calculation_method):
    factor_or_dividend = randint(0, 12)
    question = f'{factor_or_dividend} {calculation_method} {table_or_divisor} = '
    # Calling input_valid_math_answer-method to make sure input is only numbers
    user_answer = input_valid_math_answer(question, 'Use only numbers')
    if calculation_method == '*':
        correct_answer = factor_or_dividend * table_or_divisor
    elif calculation_method == '//':
        correct_answer = factor_or_dividend // table_or_divisor
    elif calculation_method == '%':
        correct_answer = factor_or_dividend % table_or_divisor
    return user_answer, correct_answer

# Method used when random calculation method is chosen
# I chose to put input in a method to make a less messy main and to avoid repetition
def calculate_random():
    # Calculation method is randomly generated
    random_calc_method = choice(['*', '//', '%'])
    factor_or_dividend = randint(0, 12)
    table_or_divisor = randint(2, 12)
    question = f'{factor_or_dividend} {random_calc_method} {table_or_divisor} = '
    # Calling input_valid_math_answer-method to make sure input is only numbers
    user_answer = input_valid_math_answer(question, 'Use only numbers')
    if random_calc_method == '*':
        correct_answer = factor_or_dividend * table_or_divisor
    elif random_calc_method == '//':
        correct_answer = factor_or_dividend // table_or_divisor
    elif random_calc_method == '%':
        correct_answer = factor_or_dividend % table_or_divisor
    return user_answer, correct_answer

# Resets values after answering wrong or killed
def reset_after_losing(num_of_questions):
    used_factor_dividend_list = [0] * 13 # Reset the list for a new game
    answered_questions = 0 # Reset for new game
    doors_left = num_of_questions # Reset num of doors left to open
    return used_factor_dividend_list, answered_questions, doors_left

# Sets up the game when playing for the first time
def start():
    n_message = 'You coward! See you another time...'
    y_message = 'Alright! Good luck in there...\n\n'

    print('************* You are locked inside a house with zombies *************')
    print('****** The only way out is to answer some mathematical questions *****')
    print('*** and to make sure not to choose the door leading to the zombies ***')
    question = ('****************** Are you ready to play? (y/n) *********************\n')
    begin = input_play_game(question, n_message, y_message)

    # While user says yes to begin
    while begin:
        # Create list for saving used values of factors or dividends
        # so they don't come up more than once
        used_factor_dividend_list = [0] * 13 # Reset the list for a new game
        answered_questions = 0

        question = 'How many questions would you like? (12-39) '
        num_of_questions = input_valid_int(question, 'Choose a number between 12-39', 12, 39)
        doors_left = num_of_questions

        question = 'Which calculation method would you like? (* // %) or random (r) '
        calculation_method = input_valid_str(question, 'Not a valid calculation method', ('*', '//', '%', 'r'))

        # Sets default values
        multiplication_table = None
        divisor = None

        # if calculation method is not 'r'
        if calculation_method in ('*', '//', '%'):
            if calculation_method == '*':
                question = 'Choose multiplication table (2-12): '
                table_or_divisor = input_valid_int(question, 'Choose a number between 2-12', 2, 12)
            elif calculation_method in ('//', '%'):
                question = 'Choose divisor (2 - 5): '
                table_or_divisor = input_valid_int(question, 'Choose a number between 2-5', 2, 5)

        print('\nAlright, let\'s play...!\n')
        begin = False
        alive = True

        # Game keeps going until alive == False and more than one door left
        while alive and doors_left > 1:
            # Zombie-door and factor/dividend is randomised
            zombie_door, factor_or_dividend = generate_new_values(doors_left)

            while True:
                # If less than 14 questions each factor/dividend only comes up once
                if num_of_questions < 14:
                    if used_factor_dividend_list[factor_or_dividend] == 0:
                        break
                 # If 14 - 25 questions each factor/dividend only comes up twice
                elif 14 <= num_of_questions < 26:
                    if used_factor_dividend_list[factor_or_dividend] < 3:
                        break
                # if 26 or more questions factor/dividend comes up three times max
                elif num_of_questions >= 26:
                    if used_factor_dividend_list[factor_or_dividend] < 4:
                        break
                # Generate new values if the current one has been used too much
                factor_or_dividend = randint(0, 12)
            # Value of factor/dividend is saved to the list
            used_factor_dividend_list[factor_or_dividend] += 1

             # If random has been selected
            if calculation_method == 'r':
                user_answer, correct_answer = calculate_random()
            else:
                user_answer, correct_answer = calculate(table_or_divisor,
                                                        factor_or_dividend, 
                                                        calculation_method)

            # Keeps track of number of answered questions
            answered_questions += 1

            # If player answers correctly they are prompted to choose a door to open
            if user_answer == correct_answer:
                print('\nCorrect!')
                question = f'Now choose a door (1-{doors_left}): '
                chosen_door = input_valid_int(question, f'You must choose a door number between 1 - {doors_left}: ', 1, doors_left)

                # If zombies are behind the door the game is over
                if chosen_door == zombie_door:
                    user_lost = True
                    print('\nOh no, the zombies killed you!\nGAME OVER')
                else:
                    # If door was ok a message is printed out
                    doors_left -= 1
                    user_lost = False
                    alive = print_good_door(zombie_door, answered_questions, doors_left)

            # If player gives wrong answer to math questions
            else:
                user_lost = True
                print('\nWrong answer - you died!\nGAME OVER')

            if user_lost:
                question = '\n*** Are you ready for another game? (y/n) ***\n'
                # Re-starts with same settings as begin is still False
                used_factor_dividend_list, answered_questions, doors_left = reset_after_losing(num_of_questions)
                # Stops loop from continuing until player has restarted
                alive = input_play_game(question, n_message, y_message)

            # If only one door left, only a math question is to be asked
            if doors_left == 1 and alive:
                print('\nCongratulations! You have made it to the final door.')
                print('To survive, you just need to make sure you answer one more question correctly\n')
                if calculation_method == 'r':
                    user_answer, correct_answer = calculate_random()
                else:
                    user_answer, correct_answer = calculate(table_or_divisor, 
                                                            factor_or_dividend, 
                                                            calculation_method)

                # If winning
                if user_answer == correct_answer:
                    print('\n*** Congratulations! ***')
                    print(f'You answered all {num_of_questions} questions correctly, and survived the zombies!\n')
                    # Game starts over from the very beginning 
                    question = '*** Are you ready for another game? (y/n) ***\n'
                    alive = False
                    begin = input_play_game(question, n_message, y_message)
                # If answering wrong on the last question
                else:
                    print('\nOh no! You were so close, but unfortunately that was the wrong answer. You will now be eaten by the zombies...\n')
                    # If player selects yes, all setings will be reset
                    # and the game starts with previous settings (begin = False)
                    question = '*** Are you ready for another game? (y/n) ***\n'
                    begin = False
                    alive = input_play_game(question, n_message, y_message)
                used_factor_dividend_list, answered_questions, doors_left = reset_after_losing(num_of_questions)


start()


