import die
import item
from adventurer import Adventurer
from map import Map

class Adventure:
    # changes to a 'current' location to go a specific direction
    NORTH = [0, -1]
    EAST = [1, 0]
    SOUTH = [0, 1]
    WEST = [-1, 0]

    def __init__(self, map_file_name, class_name):
        self.player = Adventurer('Tango', class_name) # default character
        self.player_x = 0                             # player's current x-coord
        self.player_y = 0                             # player's current y-coord
        self.world = Map(map_file_name)               # load the given map as the world for the adventure
        self.won = False                              # has the player beaten the adventure?

        self.determine_start()

    def determine_start(self):
        ''' determine_start figures out where the game will start on the map '''
        starts = self.world.get_starting_cells()
        start = starts[die.roll(len(starts))-1] # randomly choose a start location from those possible
        self.player_x, self.player_y = start

    def move_player(self, loc_mod):
        ''' move_player alters the player's location based on the given modifier '''
        self.player_x += loc_mod[0]
        self.player_y += loc_mod[1]
        # if the player moves onto a road, take the road in the same direction until a visitable cell is reached
        if self.world.cells[self.player_y][self.player_x].is_road():
            self.move_player(loc_mod)

    def start(self):
        ''' start kicks off an adventure '''
        # print(self.world)
        # print('Starting', self.player, 'at (' + str(self.player_x) + ',' + str(self.player_y) + ')')

        # keep visiting locations until the move count runs out
        moves = 20
        while not self.won and self.player.hp > 0 and moves > 0:
            self.visit_location()
            moves -= 1

        print()
        if self.won:
            print('The key unlocked the chest! You win!')
        elif moves == 0:
            print('You ran out of moves!')
        else:
            print('YOU DIED')

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
            choice = input("What would you like to do? ").lower()
            if opt.count(choice) == 0:
                print("\tInvalid choice. Try again.")
                continue

            # handle movement choice
            if choice == 'north':
                self.move_player(Adventure.NORTH)
            elif choice == 'east':
                self.move_player(Adventure.EAST)
            elif choice == 'south':
                self.move_player(Adventure.SOUTH)
            elif choice == 'west':
                self.move_player(Adventure.WEST)
            # handle interaction choice
            else:
                items = self.world.cells[self.player_y][self.player_x].items
                chest, key, pool = None, None, None
                for it in items:
                    if isinstance(it, item.Chest):
                        chest = it
                    elif isinstance(it, item.Key):
                        key = it
                    elif isinstance(it, item.RadiantPool):
                        pool = it
                # if interacting with a chest, see if there are any keys that unlock it
                if choice == 'chest':
                    for it in self.player.backpack:
                        if isinstance(it, item.Key):
                            if chest.unlocked_by(it):
                                self.won = True
                    if not self.won:
                        print('\tYou need a key to unlock this chest.')
                # interacting with a key picks it up
                elif choice == 'key':
                    print('\tYou picked up the key.')
                    self.player.backpack.append(key)
                    self.world.cells[self.player_y][self.player_x].items.remove(key)
                # a pool heals the player for a specified number of points
                elif choice == 'radiant pool':
                    hp = self.player.hp
                    pool.cleanse(self.player)
                    print('\tYou healed for', self.player.hp - hp,'hit points.')
                else:
                    print('Interacting with \'' + choice + '\'s is not supported.')
                    continue

            break # exit when a valid choice has been made

    def visit_combat(self):
        ''' visit_combat performs combat for the current cell '''
        if len(self.world.cells[self.player_y][self.player_x].npcs) == 0:
            return True

        targets = [] # list of the names of possible targets
        print('You are attacked!',end=' ')
        for enemy in self.world.cells[self.player_y][self.player_x].npcs:
            print(enemy, end=' ')
            targets.append(str(enemy).lower())
        print('enters combat with you.')

        # as long as there are combatants, fight
        while len(self.world.cells[self.player_y][self.player_x].npcs) > 0:
            # player acts first
            print('\tYou have', self.player.hp,'hp.', end=' ')
            choice = input('Attack or run? ').lower()
            if choice == 'run':
                # player has a 75% chance to successfully run
                if die.roll(4) > 1:
                    print('\t\tSuccessfully ran away.')
                    self.determine_start()
                    break
                else:
                    print('\t\tCannot escape!')

            # player attack phase
            choice = input('\tChoose a target: ').lower()
            while targets.count(choice) == 0:
                print('\tInvalid target.')
                choice = input('\tChoose a target: ').lower()

            target = self.world.cells[self.player_y][self.player_x].get_npc_by_name(choice)
            player_dmg = self.player.roll_damage()
            print('\t\tDealt',player_dmg, 'damage to',target)

            # if the target dies as a result of the damage, remove it from the cell
            if not target.take_damage(player_dmg):
                # if player levels up due to the XP
                if self.player.gain_xp(target.xp_worth()):
                    print('\t\tLevel up! You are now level', self.player.level)
                self.world.cells[self.player_y][self.player_x].npcs.remove(target)

                print('\t\t' + str(target), 'evaporated!')
                print('\t\tGained', target.xp_worth(), 'xp.')

            # all NPCs hit
            for npc in self.world.cells[self.player_y][self.player_x].npcs:
                npc_dmg = npc.roll_damage()
                print('\t\tYou took',npc_dmg,'points of damage from', npc)
                if not self.player.take_damage(npc_dmg):
                    return False
        return True

    def visit_location(self):
        ''' visit_location enables the player to visit a location '''
        # print(self.world.cells[self.player_y][self.player_x].id)
        # combat happens immediately. return if player dies
        if not self.visit_combat():
            return
        self.visit_options() # prompt user with post-combat options

    def visit_options(self):
        ''' visit_options presents the player with all post-combat options '''
        opt = self.travel_options() # directions player can travel from current location

        # output possible directions
        print('\nYou see a path to the', opt[0].capitalize(), end='')
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
    adv = Adventure('map1.txt', 'fighter')
    adv.start()
main()
