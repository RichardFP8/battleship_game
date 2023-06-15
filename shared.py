from itertools import islice


def is_there_overlap(new_ship, ships_ready):
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
                    return False
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
                    return False

        # new is vertical and other is horizontal
        if new_isVertical and not other_isVertical:
            horizontal_test = other_start_x <= new_start_x <= other_end_x
            vertical_test = new_start_y <= other_start_y <= new_end_y
            # if there's an overlap on both x and y then it's false
            if horizontal_test and vertical_test:
                return False

        # new is horizontal and other is vertical
        else:
            # ships reverse for the if-statement above
            horizontal_test = new_start_x <= other_start_x <= new_end_x
            vertical_test = other_start_y <= new_start_y <= other_end_y
            if horizontal_test and vertical_test:
                return False

    return True  # if the loop completes than its valid


def ships_on_this_line(row_height, ships_left, dropped_verticals):
    # get the ships in this line
    ships_here = {}
    for ship, info in ships_left.items():
        if info[0][1] == row_height or ship in dropped_verticals:
            ships_here[ship] = info

    sort_ships = dict(sorted(ships_here.items(), key=lambda x: x[0][0][0]))

    return sort_ships


def print_ships_on_line(row_height, ships_left, dropped_verticals, current_index):
    """Args:
        row_height: (int) the current iteration of the main loop, also represents the y coordinate
        ships_left: (dict) the ships that haven't been done printing
        dropped_verticals: (dict) the ships facing vertically that aren't done printing
        current_index: (int) tracking what ships have finished printing to update ships_left
      Print all the ships that fall on this line (row_height; based on their y-coordinates)"""

    # this variable, line, is what will be printed and returned
    line = '|'
    # if the ship falls on this line, then update current_index
    dropped_verticals_keys = dropped_verticals.keys()
    for ship, current_info in ships_left.items():
        start_x_coord, start_y_coord = current_info[0]  # starting coordinates
        end_x_coord, end_y_coord = current_info[1]  # ending coordinates
        is_vertical = current_info[2]  # used for conditional flow; know how to print the ship
        direction = current_info[3]  # to print the ship
        ship_length = current_info[4]  # horizontal ships are printed completely in one line
        line_length = len(line)  # used for rjust; print the lines at the correct indexes by correct width
        # if it's horizontal
        if row_height == end_y_coord and not is_vertical:
            draw_ship = direction * ship_length  # entire ship will be printed on this line
            # number of whitespaces between the last non-whitespace character to the next one
            width = abs(line_length - end_x_coord) + 1  # +1 means including '|' in the width
            line += draw_ship.rjust(width)
            current_index += 1

        # if is vertical, dropped and not completely done printing
        elif ship in dropped_verticals_keys:
            line += direction.rjust(abs(line_length - start_x_coord) + 1)
            if row_height == end_y_coord:  # this is where it reaches the end of its size
                del dropped_verticals[ship]  # don't include it in this dict, so we don't print it anymore
                current_index += 1

                # if is vertical, not already in dropped_verticals dictionary and starts at this line
        elif is_vertical and ship not in dropped_verticals_keys and row_height == start_y_coord:
            line += direction.rjust(abs(line_length - start_x_coord) + 1)
            dropped_verticals[ship] = ship  # add the KEY to this dict; key-value pairs are both the same value
        else:  # list is sorted by smallest y's, no need to search through ships w/ other y's than row_height
            break

    # complete the line, print it, and go to the next iteration
    # line += '|'.rjust(50 - len(line))  # find any remaining whitepsace to complete a line of 50 characters
    # print(line)
    # if len(line) > 50:
    #   print('F  A  I  L  E  D\n'.center(50))
    #   return False

    return True


def battlefield(all_ships, total_ships):
    """Args:
          all_ships: (dict) containing all the ships to print **sorted by starting y (then by starting x) coordinates
          Print the field and ships based on the input
          total_ships: (int) the number of ships to print"""

    # we need the starting y-coordinates to know when to start to drop the ship
    starting_y_points = [y[0][1] for y in all_ships.values()]
    dropped_verticals = {}  # store the ships that just started to be dropped and face vertically
    current_index = 0  # use to track the ships that haven't been dropped w/ itertools.islice()

    for row_height in range(25):
        if row_height == 0 or row_height == 24:  # First and last lines are edges
            print('-' * 50)
        # print the ship(s) that start at this y or are vertical ships
        elif row_height in starting_y_points or bool(dropped_verticals):
            # track the ships not done printing w/ current_index
            ships_left = dict(islice(all_ships.items(), current_index, total_ships))
            # inner for-loop, multiple if-conditions: print the corresponding ships on this row_height(y)
            ships_here = ships_on_this_line(row_height, ships_left, dropped_verticals)
            print(row_height)
            for ship, info in ships_here.items():
                print(ship, info)
            print()
            print_ships_on_line(row_height, ships_here, dropped_verticals, current_index)
            # check if the line completes at least in the right length, otherwise stop printing
            # if not check: return False
            continue  # move on to the next iteration of the outer loop

        # # else no ship drops, and it's not the top/bottom, just add '|'
        # else:
        #     print('|'.ljust(25) + '|'.rjust(25))

    return 0
