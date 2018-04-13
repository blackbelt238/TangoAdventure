class Adventurer(Character):
    ''' Adventurer represents a player character. It can do things such as level up and hold items '''
    def __init__(self, name, class_name):
        Character.__init__(self, 0, 0, 1, name)
        self.backpack = []             # items the character is holding
        self.class = Class(class_name) # character class
        self.xp = xp                   # all adventurers start with 0 xp

    def gain_xp(self, gained):
        ''' gain_xp enables the adventurer to gain XP, leveling him up if necessary '''
        self.xp += gained

        # if the character levels up
        if self.xp > 10:
            self.hp_max += self.class.roll_hit_die() + self.level # increase HP cap by the number of sides on the damage die
            self.level += 1                                       # gain a level
            self.xp -= 10                                         # leave only left-over XP

class Class:
    ''' Class represents an adventurer's class. It determines the character's hit die and damage di(c)e '''
    def __init__(self, name):
        self.name = name
        self.damage_die = 0     # die to use for damage rolls
        self.damage_die_num = 1 # number of dice to roll for damage
        self.hit_die = 0
        self.setup_class()

    def setup_class(self):
        if self.name == 'fighter':
            self.hit_die = 10
            # fighters attack using a 'great axe'
            self.damage_die = 12
        if self.name == 'wizard':
            self.hit_die = 6
            # wizards attack with 'burning hands'
            self.damage_die = 6
            self.damage_die_num = 3

    def roll_hit_die(self):
        ''' roll_hit_die performs an HP roll for the character (calculating HP to add to the character's max after leveling up) '''
        return die.roll(self.hit_die)
