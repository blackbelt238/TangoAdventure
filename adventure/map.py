from character import Character
from collections import defaultdict
import item

class Map:
    ''' Map represents a location for an adventurer to navigate '''
    def __init__(self, filename):
        self.cells = None       # create the place to put the Map
        self.init_map(filename) # populate the map

    def __str__(self):
        ''' the string representation of a map is just the cell ids arranged in grid form '''
        map = ''
        for row in self.cells:
            for cell in row:
                map += str(cell) + ' '
            map += '\n'
        return map

    def init_map(self, filename):
        ''' read_map goes to the given file and parses out map details '''
        map_file = open(filename,'r')  # open the map file

        # read the coordinates of the map to be read
        map_line = map_file.readline()
        m = int(map_line.split(',')[0])             # width
        n = int(map_line.split(',')[1])             # height
        self.cells = [[None] * n for i in range(m)] # make a map skeleton the size of the eventual map

        # create the cells that make up the map
        for row in range(len(self.cells)):
            cell_info = map_file.readline().split() # get information from file for this row
            for col in range(len(self.cells[row])):
                self.cells[row][col] = Cell(cell_info[col]) # instantiate a Cell with the id logged in the cell_info

        info = self.read_map_info(map_file) # get all the information to be added to the map (chars, items, etc.)
        map_file.close()                    # close the map file
        self.populate_map(info)             # populate the map with the infomration from the file

    def populate_map(self, info):
        ''' populate_map takes the given information and adds it into the map '''
        return

    def read_map_info(self, map_file):
        ''' read_map_info reads the remainder of the map file to extract the information to be added to the map '''
        info = defaultdict(list) # all information to be added to the map

        # while there is still information, store it in the info dict
        map_line = map_file.readline()
        while map_line:
            new_info = None # information to be added to the map

            # separate the cell that the info relates to from the rest of the info
            n = map_line.split(':')
            cell_num, map_line = n[0], n[1]

            # extract the type of information we are adding to the cell from the information
            t = map_line.split('|')
            info_type, map_line = t[0], t[1] # remove the remaining bracket for data integrity

            # based on the type of the information to add, build the information
            if info_type == 'character':
                attrs = map_line.split()
                damage_die = int(attrs[0])
                hp = int(attrs[1])
                level = int(attrs[2])
                name = attrs[3]
                xp = int(attrs[4])

                new_info = Character(damage_die, hp, level, name, xp)
            elif info_type == 'item':
                attrs = map_line.split()
                item_type = attrs[0]
                if item_type == 'chest':
                    new_info = item.Chest(int(attrs[1]))
                elif item_type == 'key':
                    new_info = item.Key(int(attrs[1]))
                elif item_type == 'radiantpool':
                    new_info = item.RadiantPool()
                else:
                    new_info = item_type
                    return
            else:
                # directly add any other info
                new_info = info_type

            info[cell_num].append(new_info) # add the new information
            map_line = map_file.readline()
        return info

class Cell:
    ''' Cell represents a single visitable location in a Map '''
    def __init__(self, id):
        self.id = id    # id of the cell
        self.items = [] # items in the cell
        self.npcs = []  # characters in the cell
        self.start = False

    def __str__(self):
        return self.id

    def add_character(self, character):
        ''' add_character adds the given character to the list of NPCs on this cell '''
        self.npcs.append(character)

    def add_item(self, item):
        ''' add_item adds the given item to the list of items in this cell '''
        self.items.append(item)

    def is_passthrough(self):
        ''' is_passthrough determines if the cell is one that is passed through during traversal.
            A passthrough cell is not visited, it is simply used to access visitable cells '''
        return self.id == '_'

    def is_wall(self):
        ''' is_wall determines if this cell is a wall '''
        return self.id == '#'

def main():
    m = Map('map1.txt')
    print(m, end='')

main()
