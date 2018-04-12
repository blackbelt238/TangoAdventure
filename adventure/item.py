class Item:
    ''' Item represents an encounterable item within the adventure '''
    def __init__(self, t):
        self.type = t # the item's type

    def __str__(self):
        return self.type

class Chest(Item):
    ''' Chest represents the win condition for the game '''
    def __init__(self, number):
        Item.__init__(self, 'chest')
        self.number = number # this chest's number

    def unlocked_by(self, key):
        ''' unlocked_by determines if the given key unlocks this chest.
            A key only unlocks a chest if it has the same number as the chest. '''
        return self.number == key.number

class Key(Item):
    ''' Key represents an item that opens a chest '''
    def __init__(self, number):
        Item.__init__(self, 'key')
        self.number = number # chest number that this key unlocks

class RadiantPool(Item):
    def __init__(self):
        Item.__init__(self, 'radiant pool')

    def cleanse(self, character):
        character.heal_for(100)
