from random import randint
from shared import *


def create_one_ship():
    """Create the coordinates, whether its vertical, and the length of the ship"""
    # create the starting cooridinates
    dropHere_x = randint(1, 48)
    dropHere_y = randint(1, 23)
    direction = randint(1, 4)
    size = randint(2, 7)  # length of the ship
    is_vertical = direction == 1 or direction == 4
    ship_direction = ''  # where will the ship point in the field
    match direction:
        case 1:
            ship_direction = '^'
        case 2:
            ship_direction = '>'
        case 3:
            ship_direction = '<'
        case 4:
            ship_direction = 'v'

    # track the end points of the ships
    end_point_y = size + dropHere_y
    end_point_x = size + dropHere_x

    #  test that the ship fits in the map, in x-axis & y-axis
    if is_vertical and end_point_y > 23:
        dropHere_y -= end_point_y - 23  # change y to fit the ship in the field

    if not is_vertical and end_point_x > 49:
        dropHere_x -= end_point_x - 49

    starting_points = (dropHere_x, dropHere_y)
    # size - 1 means that the ending point is exact: ex size = 3, start_x = 2,
    ending_points = (dropHere_x, dropHere_y + size - 1) if is_vertical \
        else (dropHere_x + size - 1, dropHere_y)
    # store the ship's info into one list
    return [starting_points, ending_points, is_vertical, ship_direction, size]


def create_all_ships(ships_needed):
    """Args:
        ships_needed: (int) from 2-10; how many ships to create
        Based on the input this function creates single ships and adds them to a dictionary,
        then each one is validated by the ships already in the dictionary so there's no overlap.
        Unless of course, it's the first ship"""

    com_ships = {}  # keep all the ship's data here
    ship_count = 1  # the auto-increment number for each ship
    if ships_needed > 10 or ships_needed < 1:
        print('Input should be between 2-10')
        return 0

    for ship in range(1, ships_needed + 1):
        ship_data = create_one_ship()
        # for the first ship, no problem
        if len(com_ships) == 0:
            com_ships['ship1'] = ship_data
        else:
            # validate that the new ship doesn't overlap with the other ship(s)
            while not is_there_overlap(ship_data, com_ships):
                # if it isn't valid, create a new ship and validate that one
                ship_data = create_one_ship()
            com_ships[f'ship{ship_count}'] = ship_data

        ship_count += 1  # auto-increment the ship count

    # sort by starting y(and then starting x) coordinates to loop through them more easily when printing lines
    sorted_ships = dict(sorted(com_ships.items(), key=lambda x: (x[1][0][1], x[1][0][0])))
    return sorted_ships


def computer_main(num_ships):
    all_ships = create_all_ships(num_ships)
    battlefield(all_ships, num_ships)
