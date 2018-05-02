import die
import item
from adventurer import Adventurer
from client import Client
from map import Map
from playerbot import Playerbot

class Adventure:
    # changes to a 'current' location to go a specific direction
    NORTH = [0, -1]
    EAST = [1, 0]
    SOUTH = [0, 1]
    WEST = [-1, 0]

    def __init__(self, map_file_name, class_name):
        self.player = Adventurer('Tango', class_name) # default character
        self.bot = Playerbot()                        # the robot the player will interact with
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

        self.bot.move(loc_mod)

        # if the player moves onto a road, take the road in the same direction until a visitable cell is reached
        if self.world.cells[self.player_y][self.player_x].is_road():
            self.move_player(loc_mod)

    def start(self):
        ''' start kicks off an adventure '''
        # keep visiting locations until the move count runs out
        moves = 20
        while not self.won and self.player.hp > 0 and moves > 0:
            self.visit_location()
            moves -= 1

        # based on how game ended, inform Android
        if self.won:
            Client.sendMessage('win')
        elif moves == 0:
            Client.sendMessage('no moves')
        else:
            Client.sendMessage('died')

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
        # ask Android for user's choice. no validation necessary because Android will only present user with valid options
        choice = Client.sendMessage('action:'+str(opt))
        print("\taction choice:", choice)

        # set up items for interaction
        items = self.world.cells[self.player_y][self.player_x].items
        chest, pool = None, None # possible items to interact with on the cell
        for it in items:
            if isinstance(it, item.Chest):
                chest = it
            elif isinstance(it, item.Key):
                self.player.backpack.append(it)                                 # keys are automatically picked up
                self.world.cells[self.player_y][self.player_x].items.remove(it) # remove the key from the cell once player picks it up
                print('\t***********PICKED UP KEY******************')
            elif isinstance(it, item.RadiantPool):
                pool = it

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
            # if interacting with a chest, see if the player has any keys that unlock it
            if choice == 'chest':
                for it in self.player.backpack:
                    if isinstance(it, item.Key):
                        if chest.unlocked_by(it):
                            self.won = True
                if not self.won:
                    Client.sendMessage('need key') # inform Android that the player does not have the right key
            # a pool heals the player for a specified number of points
            elif choice == 'pool':
                pool.cleanse(self.player)

    def visit_combat(self):
        ''' visit_combat performs combat for the current cell '''
        if len(self.world.cells[self.player_y][self.player_x].npcs) == 0:
            return True # skip combat if there's nobody to fight

        targets = [] # list of the names of possible targets
        for enemy in self.world.cells[self.player_y][self.player_x].npcs:
            targets.append(str(enemy).lower())
        Client.sendMessage('combat:'+str(targets)) # inform Android combat has started
        self.bot.encounter()

        # as long as there are combatants, fight
        while len(self.world.cells[self.player_y][self.player_x].npcs) > 0:
            # player acts first
            choice = Client.sendMessage('hp:'+str(self.player.hp)) # expect 'attack' or 'run'
            print('\tcombat choice:\'' + choice +'\'')
            if choice == 'run':
                # player has a 75% chance to successfully run
                if die.roll(4) > 1:
                    Client.sendMessage('run:true') # tell Android run was successful
                    self.determine_start()      # teleport the player off to a starting location
                    break
                else:
                    Client.sendMessage('run:false') # tell Android run was not successful

            # player attack phase
            # choice = Client.sendMessage('target') # ask Android for a valid target
            target = self.world.cells[self.player_y][self.player_x].get_npc_by_name(targets[0]) # step 2 only allows 1 opponent per cell
            player_dmg = self.player.roll_damage()
            self.bot.hit()
            Client.sendMessage('dealt:'+str(player_dmg))

            # if the target dies as a result of the damage, remove it from the cell and from list of possible targets
            if not target.take_damage(player_dmg):
                self.world.cells[self.player_y][self.player_x].npcs.remove(target)
                targets.remove(target.name)
                Client.sendMessage('gained:'+str(target.xp_worth()))

            # NPC attack phase
            for npc in self.world.cells[self.player_y][self.player_x].npcs:
                npc_dmg = npc.roll_damage()
                Client.sendMessage('recv:'+str(npc_dmg)) # tell Android how much damage player was dealt to the player
                if not self.player.take_damage(npc_dmg):
                    return False
        return True

    def visit_location(self):
        ''' visit_location enables the player to visit a location '''
        # combat happens immediately. return if player dies
        if not self.visit_combat():
            return
        self.visit_options() # prompt user with post-combat options

    def visit_options(self):
        ''' visit_options presents the player with all post-combat options '''
        opt = self.travel_options() # directions player can travel from current location

        # output items
        for item in self.world.cells[self.player_y][self.player_x].items:
            opt.append(str(item))

        # prompt user and take action
        self.visit_action(opt)

def main():
    class_name = Client.sendMessage('class') # expecting 'figher' or 'wizard'
    print('starting the adventure with a', class_name)
    adv = Adventure('adventure/map2.txt', class_name)
    adv.start()
main()
