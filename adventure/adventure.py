import die
from adventurer import Adventurer
from map import Map

class Adventure:
    # changes to a 'current' location to go a specific direction
    NORTH = [0, -1]
    EAST = [1, 0]
    SOUTH = [0, 1]
    WEST = [-1, 0]

    def __init__(self, map_file_name, create_character):
        self.player = Adventurer('Tango', 'fighter') # default character
        self.player_x = 0                            # player's current x-coord
        self.player_y = 0                            # player's current y-coord
        self.world = Map(map_file_name)              # load the given map as the world for the adventure

        self.determine_start()
        if create_character:
            self.create_character()

    def create_character(self):
        return

    def determine_start(self):
        ''' determine_start figures out where the game will start on the map '''
        starts = self.world.get_starting_cells()
        start = starts[die.roll(len(starts))-1] # randomly choose a start location from those possible
        self.player_x, self.player_y = start

    def move_player(self, loc_mod):
        ''' move_player alters the player's location based on the given modifier '''
        self.player_x += loc_mod[0]
        self.player_y += loc_mod[1]

    def start(self):
        ''' start kicks off an adventure '''
        # print(self.world)
        # print('Starting', self.player, 'at (' + str(self.player_x) + ',' + str(self.player_y) + ')')

        # keep visiting locations until the move count runs out
        moves = 0
        while moves < 5:
            self.visit_location()
            moves += 1
        print('You ran out of moves!')

    def travel_options(self):
        ''' travel_options returns a list of valid options for leaving the current cell '''
        opt = []

        # north
        if not (self.player_y-1 < 0) and self.world.cells[self.player_y-1][self.player_x].id != '#':
            opt.append('north')
        # east
        if not (self.player_x+1 > len(self.world.cells[self.player_y])-1) and self.world.cells[self.player_y][self.player_x+1].id != '#':
            opt.append('east')
        # south
        if not (self.player_y+1 > len(self.world.cells)-1) and self.world.cells[self.player_y+1][self.player_x].id != '#':
            opt.append('south')
        # west
        if not (self.player_x-1 < 0) and self.world.cells[self.player_y][self.player_x-1].id != '#':
            opt.append('west')
        return opt

    def visit_action(self, opt):
        ''' visit_action handles the user's choice of action '''
        while True:
            # take in user choice and check if valid
            choice = input("\nWhat would you like to do? ").lower()
            if opt.count(choice) == 0:
                print("Invalid choice. Try again.", end='')
                continue

            # handle choice
            if choice == 'north':
                self.move_player(Adventure.NORTH)
            elif choice == 'east':
                self.move_player(Adventure.EAST)
            elif choice == 'south':
                self.move_player(Adventure.SOUTH)
            elif choice == 'west':
                self.move_player(Adventure.WEST)
            else:
                print('cant do items right now')
                continue

            break

    def visit_combat(self):
        ''' visit_combat performs combat for the current cell '''

    def visit_location(self):
        ''' visit_location enables the player to visit a location '''
        # print(self.world.cells[self.player_y][self.player_x].id)
        self.visit_combat()  # combat happens immediately
        self.visit_options() # prompt user with post-combat options

    def visit_options(self):
        ''' visit_options presents the player with all post-combat options '''
        opt = self.travel_options() # directions player can travel from current location

        # output possible directions
        print('You see a path to the', opt[0].capitalize(), end='')
        for i in range(1, len(opt)):
            print(',', opt[i].capitalize(), end = '')
        print('.')

        # output items
        if len(self.world.cells[self.player_y][self.player_x].items) > 0:
            print('On the ground in front of you is a ', end='')
            for i, item in enumerate(self.world.cells[self.player_y][self.player_x].items):
                if i > 0:
                    print(',', end=' ')
                opt.append(str(item))
                print(str(item).title(), end='')
            print('.')

        # prompt user and take action
        self.visit_action(opt)

def main():
    adv = Adventure('map1.txt', False)
    adv.start()
main()
