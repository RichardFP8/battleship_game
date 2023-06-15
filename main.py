# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randint
from itertools import islice


def create_one_ship():
    """Create the coordinates, whether its vertical, and the length of the ship"""
    # create the starting cooridinates
    dropHere_x = randint(1, 48)
    dropHere_y = randint(1, 23)
    direction = randint(1, 4)
    size = randint(2, 7)  # length of the ship
    isVertical = direction == 1 or direction == 4
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
    if isVertical and end_point_y > 23:
        dropHere_y -= end_point_y - 23  # change y to fit the ship in the field

    if not isVertical and end_point_x > 49:
        dropHere_x -= end_point_x - 49

    starting_points = (dropHere_x, dropHere_y)
    # size - 1 means that the ending point is exact: ex size = 3, start_x = 2,
    ending_points = (dropHere_x, dropHere_y + size - 1) if isVertical \
        else (dropHere_x + size - 1, dropHere_y)
    # store the ship's info into one list
    return [starting_points, ending_points, isVertical, ship_direction, size]


def is_ship_valid(new_ship, ships_ready):
    """Test that the new ship won't overlap with any other ship already in the group of ships.
        Both vertical/horizontal or one ship is one and vice-versa(4 cases)
        Args:
            new_ship: the data of the new potential ship joining the group of ships
            ships_ready: the dictionary that contains all the data of the group of ships"""

    # get the info of the new ship
    new_start_x, new_start_y = new_ship[0]  # the starting coordinates
    new_end_x, new_end_y = new_ship[1]  # the ending coordinates
    new_isVertical = new_ship[2]
    # test the new ship with all the ships for overlap
    for ship_name, other_ship in ships_ready.items():
        # get the info of the ships already in the dictionary
        other_start_x, other_start_y = other_ship[0]
        other_end_x, other_end_y = other_ship[1]
        other_isVertical = other_ship[2]

        # both are vertical
        if new_isVertical and other_isVertical:
            # both have different x values, on to the next ship if any
            if new_start_x != other_start_x:
                continue
            else:
                # either end of the new ship in between the ends of the other ship
                first_interval = other_start_y <= new_start_y <= other_end_y
                second_interval = other_start_y <= new_end_y <= other_end_y
                if first_interval or second_interval:
                    # print('VV First', other_start_y, new_start_y, other_end_y)
                    return False
                # if second_interval:
                #   print('VV Sec', other_start_y, new_end_y, other_end_y)
                #   return False
        # both are horizontal
        if not new_isVertical and not other_isVertical:
            # both have different y values, on to next ship if any
            if new_start_y != other_start_y:
                continue
            else:
                # check if there are no overlaps between the ships
                first_interval = other_start_x <= new_start_x <= other_end_x
                second_interval = other_start_x <= new_end_x <= other_end_x
                if first_interval or second_interval:
                    # print('HH First', other_start_x, new_start_x, other_end_x)
                    return False
                # if second_interval:
                #   print('HH Sec', other_start_x, new_end_x, other_end_x)
                #   return False

        # new is vertical and other is horizontal
        if new_isVertical and not other_isVertical:
            horizontal_test = other_start_x <= new_start_x <= other_end_x
            vertical_test = new_start_y <= other_start_y <= new_end_y
            # if there's an overlap on both x and y then it's false
            if horizontal_test and vertical_test:
                # print(f'VH:{other_start_x} <= {new_start_x} <= {other_end_x}')
                # print(f'VH:{new_start_y} <= {other_start_y} <= {new_end_y}')
                return False

        # new is horizontal and other is vertical
        else:
            # ships reverse for the if-statement above
            horizontal_test = new_start_x <= other_start_x <= new_end_x
            vertical_test = other_start_y <= new_start_y <= other_end_y
            if horizontal_test and vertical_test:
                # print(f'HV:{new_start_x} <= {other_start_x} <= {new_end_x}')
                # print(f'HV:{other_start_y} <= {new_start_y} <= {other_end_y}')
                return False

    return True  # if the loop completes than its valid


def create_all_ships(ships_needed):
    """Args:
        ships_needed: (int) from 2-10; how many ships to create
        Based on the input this function creates single ships and adds them to a dictionary,
        then each one is validated by the ships already in the dictionary so there's no overlap.
        Unless of course, it's the first ship"""

    created_ships = 0  # track how many ships were created
    all_ships = {}  # keep all the ship's data here
    ship_count = 1  # the auto-increment number for each ship
    if ships_needed > 10 or ships_needed < 1:
        print('Input should be between 2-10')
        return 0

    while created_ships < ships_needed:
        ship_data = create_one_ship()
        # for the first ship, no problem
        if len(all_ships) == 0:
            all_ships['ship1'] = ship_data
        else:
            # validate that the new ship doesn't overlap with the other ship(s)
            while not is_ship_valid(ship_data, all_ships):
                # if it isn't valid, create a new ship and validate that one
                ship_data = create_one_ship()
            all_ships[f'ship{ship_count}'] = ship_data

        ship_count += 1  # auto-increment the ship count
        created_ships += 1  # one ship is created

    # sort by starting y(and then starting x) coordinates to loop through them more easily when printing lines
    sorted_ships = dict(sorted(all_ships.items(), key=lambda x: (x[1][0][1], x[1][0][0])))
    return sorted_ships


def battlefield(all_ships, total_ships):
    """Args:
          all_ships: (dict) containing all the ships to print **sorted by starting y (then by starting x) coordinates
          Print the field and ships based on the input
          total_ships: (int) the number of ships to print"""

    # we need the starting y-coordinates to know when to start to drop the ship
    starting_y_points = [y[0][1] for y in all_ships.values()]
    dropped_verticals = {}  # store the ships that just started to be dropped and face vertically
    current_index = 0  # use to track the ships that haven't been dropped w/ itertools.islice()

    for bar_height in range(25):
        if bar_height == 0 or bar_height == 24:  # First and last lnes are edges
            print('-' * 50)
        # print the ship(s) that start at this y
        elif bar_height in starting_y_points or bool(dropped_verticals):
            # this line variable is what will be printed and returned
            line = '|'
            # if the ship falls on this line, then update current_index
            ships_left = dict(islice(all_ships.items(), current_index, total_ships))
            dropped_verticals_keys = dropped_verticals.keys()
            for ship, current_info in ships_left.items():
                # use for conditionals
                start_x_coord, start_y_coord = current_info[0]  # starting points
                end_x_coord, end_y_coord = current_info[1]  # ending points
                is_vertical = current_info[2]  # used for conditional flow; know how to print the ship
                direction = current_info[3]  # to print the ship
                ship_length = current_info[4]  # horizontal ships are printed completely in one line
                line_length = len(line)  # used for rjust; print the lines at the correct indexes by correct width
                # if it's horizontal
                if bar_height == end_y_coord:
                    draw_ship = direction * ship_length  # entire ship will be printed on this line
                    # number of whitespaces between the last non-whitespace character to the next one
                    width = abs(line_length - end_x_coord) + 1  # +1 means including '|' in the width
                    line += draw_ship.rjust(width)
                    current_index += 1

                # if is vertical, dropped and not completely done printing
                elif ship in dropped_verticals_keys:
                    line += direction.rjust(abs(line_length - start_x_coord) + 1)
                    current_index += 1
                    if bar_height + 1 == end_y_coord:  # this is where it reaches the end of its size
                        del dropped_verticals[ship]  # don't include it in this dict, so we don't print it anymore

                # if is vertical, not already in dropped_verticals dictionary and starts at this line
                elif is_vertical and ship not in dropped_verticals_keys and bar_height == start_y_coord:
                    line += direction.rjust(abs(line_length - start_x_coord) + 1)
                    dropped_verticals[ship] = ship  # add the KEY to this dict; key-value pairs are both the same value
                    current_index += 1
                else:  # list is sorted by smallest y's, no need to search through ships w/ other y's than bar_height
                    break

            # complete the line, print it, and go to the next iteration
            line += '|'.rjust(50 - len(line))  # find any remaining whitepsace to complete a line of 50 characters
            if len(line) > 50:
                return False
            print(line)
            continue  # move on to the next iteration of the outer loop

        # else no ship drops, and it's not the top/bottom, just add '|'
        else:
            print('|'.ljust(25) + '|'.rjust(25))

    return 0


if __name__ == '__main__':
    num = 5
    # all_ships = create_all_ships(num)
    # battlefield(all_ships, num)

    for x in range(3):
        all_ships = create_all_ships(num)
        battlefield(all_ships, num)

        for ship, info in all_ships.items():
            print(ship, info)
    # my_dict = {1:2, 3:4, 5:6, 7:8}
    # other = dict(islice(my_dict.items(), 2, 4))

    # -----------                               USE DATA FOR TESTS
    # ship4[(27, 5), (30, 5), False, '<', 3]
    # ship1[(43, 5), (49, 5), False, '<', 6]
    # ship2[(20, 6), (26, 6), False, '<', 6]
    # ship5[(39, 17), (39, 23), True, '^', 6]
    # ship3[(6, 20), (6, 23), True, '^', 3]

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
