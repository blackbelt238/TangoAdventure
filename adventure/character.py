import die

class Character:
    ''' Character represents an agent in the adventure '''
    def __init__(self, damage_die, damage_dice_num, hp_max, level, name):
        self.damage_die = damage_die          # die to use for damage rolls
        self.damage_dice_num = damage_dice_num # number of damage dice to roll
        self.hp_max = hp_max                  # max points of damage a character can endure; determined from class
        self.hp = self.hp_max                 # current hit points; start at full health
        self.level = level                    # character level buffs damage rolls
        self.name = name

    def __str__(self):
        return self.name

    def heal_for(self, points):
        ''' heal_for heals the character the given amount '''
        self.hp += points
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def roll_damage(self):
        ''' roll_damage performs a damage roll for the character (calculating damage dealt in a specific instance).
            'Roll' the character's damage dice and then add the character's level to the result. '''
        damage = 0
        # roll as many damage dice as required
        for _ in range(self.damage_die_num):
            damage += die.roll(self.damage_die)
        return damage + self.level

    def take_damage(self, points):
        ''' take_damage causes the character to lose the given amount of HP '''
        self.hp -= points
        return self.hp > 0 # returns True if the character survived the damage

    def xp_worth(self):
        ''' xp_worth calculates how much XP a character is worth '''
        return self.level
