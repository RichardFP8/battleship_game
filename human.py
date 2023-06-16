from os import system, name  # clear the console
from shared import *  # need to validate new ships and print them
from time import sleep  # let user see what's printed for a while before clearing


def how_many_ships_to_create():
    num = 0
    while not 2 <= num <= 10:
        try:
            num = int(input('How many ships to create (2-10): '))
        except ValueError:
            print('Invalid character for an integer, try again')

    return num


def clear():
    """Based on OS, clear the console after the rules been shown"""
    if name == 'nt':  # operating system is Windows
        _ = system('cls')  # else it's Linux, MacOS
    else:
        _ = system('clear')


def validate_integer(axis=''):
    """Args:
        axis: (str) Letter to find what range we're using to validate user input including leaving it empty
        Range for x is 1-48, Range for y is 1-23, Range for length of ship is 2-7 """
    number = 0
    max_num = 48 if axis == 'x' else 23 if axis == 'y' else 7
    min_num = 1 if axis else 2  # if axis isn't empty than we're validating a coordinate
    message = f'Starting coordinate for {axis} (1-{max_num}): ' if axis else 'Length of the ship (2-7): '

    while not min_num <= number <= max_num:
        try:
            number = int(input(message))
        except ValueError:
            print('Valid integer please')

    print()  # seperate the lines a bit
    return number


def is_out_of_bounds(is_vertical, x, y, length):
    """Args:
        is_vertical: (boolean) is the ship facing vertical or not
        x: (int) the starting x coordinate of the ship | (x, y) in a like-cartesian plane
        y: (int) the starting y coordinate of the ship
        length: (int) the length of the ship"""

    # check that the ship stays within the 'field' and doesn't go out
    ending_y_coord = y + length
    ending_x_coord = x + length
    out_of_bounds_vertical = is_vertical and ending_y_coord > 24
    out_of_bounds_horizontal = not is_vertical and ending_x_coord > 48

    if out_of_bounds_vertical:
        print('Y goes out of bounds, max Y is 23')
        return []

    elif out_of_bounds_horizontal:
        print('X goes out of bounds, max X is 48')
        return []

    ending_coords = (ending_x_coord, ending_y_coord)
    return ending_coords  # if it doesn't go over bounds


def create_one_ship():
    """Prompt the user for and validate the starting (x, y) coordinate, length of ship and whether it's vertical"""
    start_x_coord = validate_integer('x')
    start_y_coord = validate_integer('y')
    ship_length = validate_integer()
    is_vertical_response = ''

    # while it's not either characters keep asking
    while is_vertical_response not in ['Y', 'N']:
        is_vertical_response = input('Is the ship vertical? [Y/N]: ').upper()
    is_vertical = is_vertical_response == 'Y'

    # check if the coordinates are not 'out of bounds'
    # - 1 b/c we're including the starting x/y as part of the ship length
    # #ex: if it's 45 and length is 2, then 45 and 46 not 45, 46, 47
    ending_coords = is_out_of_bounds(is_vertical, start_x_coord, start_y_coord, ship_length - 1)
    # it means that user gave me invalid input
    if len(ending_coords) == 0:
        return []

    return [(start_x_coord, start_y_coord), ending_coords, is_vertical, "o", ship_length]


def explain_rules():
    rules = {
        'explain_1': 'You\'ll be prompted to type how many ships to create, \
                you can only create as much as 10 and at least 2',
        'explain_2': 'For each ship, you will define it\'s starting coordinates, meaning (x, y)',
        'explain_3': 'You have to also define how long the ship is, that is, it\'s length',
        'explain_4': 'Also whether the ship faces vertical or not',
        'rule_1': 'Length of ships can only be integers between 2-7 including 2 and 7',
        'rule_2': 'Starting X coordinates can only be integers between 1-48 including 1 and 48',
        'rule_3': 'Starting Y coordinates can only be integers between 1-23 including 1 and 23\n',
        'example': 'Example: If the starting coordinates are (7, 1), length is 4, and is vertical, \
                then the ending is (7, 4) b/c we\'re including y=1\n',
        'confirm_1': 'You\'ll be given a chance to look at the positions of your ships after they have been validated\n\
                This will be helpful to make sure that none of your ships overlap with one another so keep that in mind'
    }
    count = 0
    for rule in rules.values():
        match count:
            case 0:
                print('Explaination\n')
            case 4:
                print('\nRules\n')

        print(rule)
        count += 1
        sleep(7)

    sleep(5)
    clear()


def human_main():
    """Give instructions to the user playing and print their battleships"""
    # explain_rules()
    total_ships = how_many_ships_to_create()
    clear()
    user_ships = {}  # store user's ships
    ship_count = 1  # keep track of how many ships are created

    for ship in range(1, total_ships + 1):
        key = f'ship{ship_count}'  # key for the key-value pair of this ship
        print('Creating', key, '\n')  # let user know what ship we're making
        ship_data = []
        # it would return 0 if user input is invalid
        while len(ship_data) == 0:
            ship_data = create_one_ship()

        if len(user_ships) == 0:  # this must be the first ship so just add it
            user_ships[key] = ship_data
        else:
            # validate that the new ship doesn't overlap with the other ship(s)
            while not is_there_overlap(ship_data, user_ships):
                # if it isn't valid, create a new ship and validate that one
                ship_data = create_one_ship()
            user_ships[key] = ship_data

        battlefield(user_ships, total_ships)
        print(f'Successfully created {key}: {ship_data}')
        if ship_count < total_ships:
            ready_for_next = False
            while not ready_for_next and ship_count != total_ships:
                ready_for_next = input('Press Y when ready to create next ship: ').upper() == 'Y'
        clear()
        ship_count += 1

    return total_ships
