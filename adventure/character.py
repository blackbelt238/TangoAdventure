import die

class Character:
    ''' Character represents an agent in the adventure '''

    def __init__(self, damage_die, hp, level, name, xp):
        self.damage_die = damage_die # die to use for damage rolls
        self.hp = hp                 # current hit points; start at full health
        self.hp_max = hp             # max number of points of damage a character can endure
        self.level = level           # character level buffs damage rolls
        self.name = name
        self.xp = xp                 # all characters start with 0 xp

    def gain_xp(self, gained):
        ''' gain_xp enables the character to gain XP, leveling the character up if necessary '''
        self.xp += gained
        # if the character levels up
        if self.xp > 10:
            self.level += 1       # increase the level
            self.xp -= 10        # leave only left-over XP
            self.hp += self.level # increase HP by the character's level

    def heal_for(self, points):
        ''' heal_for heals the character the given amount '''
        self.hp += points
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def roll_damage(self):
        ''' roll_damage performs a damage roll for the character (calculating damage dealt in a specific instance).
            'Roll' the character's damage die and then add the character's level to the result. '''
        return die.roll(self.damage_die) + self.level

    def take_damage(self, points):
        ''' take_damage causes the character to lose the given amount of HP '''
        self.hp -= points
        return self.hp > 0 # returns True if the character survived the damage

    def xp_worth(self):
        ''' xp_worth calculates how much XP a character is worth '''
        return level
