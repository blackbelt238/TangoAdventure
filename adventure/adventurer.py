from character import Character

class Adventurer(Character):
    ''' Adventurer represents a player character. It can do things such as level up and hold items '''
    def __init__(self, name, class_name):
        Character.__init__(self, 0, 1, 0, 1, name)
        self.backpack = []          # items the character is holding
        self.character_class = None
        self.xp = 0                 # all adventurers start with 0 xp
        self.init_class(class_name) # initialize the character's class

    def __str__(self):
        return self.name + ' the ' + str(self.character_class)

    def gain_xp(self, gained):
        ''' gain_xp enables the adventurer to gain XP, leveling him up if necessary '''
        self.xp += gained

        # if the character levels up
        if self.xp > 10:
            self.hp_max += self.character_class.roll_hit_die() + self.level # increase HP cap by the number of sides on the damage die
            self.level += 1                                                 # gain a level
            self.xp -= 10                                                   # leave only left-over XP

    def init_class(self, class_name):
        ''' init_class initializes/updates an adventurer's information based on his chosen class '''
        self.character_class = Class(class_name)

        # update character info using class stats
        self.damage_die = self.character_class.damage_die
        self.damage_dice_num = self.character_class.damage_dice_num
        self.hp_max = self.character_class.hit_die
        self.hp = self.hp_max

class Class:
    ''' Class represents an adventurer's class. It determines the character's hit die and damage di(c)e '''
    def __init__(self, name):
        self.damage_die = None  # die to use for damage rolls
        self.damage_dice_num = 1 # number of dice to roll for damage
        self.hit_die = None
        self.name = name
        self.setup_class()

    def __str__(self):
        return self.name.capitalize()

    def roll_hit_die(self):
        ''' roll_hit_die performs an HP roll for the character (calculating HP to add to the character's max after leveling up) '''
        return die.roll(self.hit_die)

    def setup_class(self):
        if self.name == 'fighter':
            self.hit_die = 10
            # fighters attack using a 'great axe'
            self.damage_die = 12
        if self.name == 'wizard':
            self.hit_die = 6
            # wizards attack with 'burning hands' spell
            self.damage_die = 6
            self.damage_dice_num = 3
