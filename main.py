from shared import battlefield  # this is the only function I need
from human import main # emplicitly chose 1 function but still uses the other
from computer import create_all_ships  # emplicitly chose 1 function but still uses the other

if __name__ == '__main__':
    main()
    num = 5 # how many ships to create for computer
    for x in range(9):
        all_ships = create_all_ships(num)
        battlefield(all_ships, num)

