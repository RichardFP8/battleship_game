from human import human_main, sleep
from computer import computer_main

if __name__ == '__main__':
    ships_created = human_main()  # user goes first
    print("Computer is building...")
    sleep(2)
    computer_main(ships_created)  # print computer's ships after
