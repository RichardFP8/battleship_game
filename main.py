from shared import battlefield  # this is the only function I need
from computer import create_all_ships  # emplicitly chose 1 function but still uses the other

if __name__ == '__main__':
    num = 5
    for x in range(9):
        all_ships = create_all_ships(num)
        battlefield(all_ships, num)

#     for ship, info in all_ships.items():
#       print(ship, info)

# -----------   USE DATA FOR TESTS
# ship4[(27, 5), (30, 5), False, '<', 3]
# ship1[(43, 5), (49, 5), False, '<', 6]
# ship2[(20, 6), (26, 6), False, '<', 6]
# ship5[(39, 17), (39, 23), True, '^', 6]
# ship3[(6, 20), (6, 23), True, '^', 3]

# def Merge(dict1, dict2):
#     res = dict1 | dict2
#     return res

# # Driver code
# dict1 = {'a': {'a': 10, 'b': 4}, 'y': 8}
# dict2 = {'a': 'a', 'b': 4}
# dict3 = Merge(dict1, dict2) 
# print(dict3)