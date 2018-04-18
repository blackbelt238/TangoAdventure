import die
from adventurer import Adventurer
from map import Map

class Adventure:
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
        self.move_player(start[0], start[1])

    def move_player(self, new_x, new_y):
        ''' move_player sets the player's location to the given location '''
        self.player_x, self.player_y = new_x, new_y

    def start(self):
        ''' start kicks off an adventure '''
        print(self.world)
        print('Starting', self.player, 'at (' + str(self.player_x) + ',' + str(self.player_y) + ')')

    def visit_location(self):
        # Combat
        # Loop thru options

def main():
    adv = Adventure('map1.txt', False)
    adv.start()
main()
