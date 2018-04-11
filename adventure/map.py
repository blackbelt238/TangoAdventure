class Map:
    ''' Map represents a location for an adventurer to navigate '''
    def __init__(self, filename):
        self.cells = None       # create the place to put the Map
        self.init_map(filename) # populate the map

    def __str__(self):
        ''' the string representation of a map is just the cell ids arranged in grid form '''
        s = ''
        for row in self.cells:
            for cell in row:
                s += str(cell) + ' '
            s += '\n'
        return s

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

        self.populate_map(map_file) # populate the map with characters and items
        map_file.close()            # close the

    def populate_map(self, map_file):
        return

class Cell:
    ''' Cell represents a single visitable location in a Map '''
    def __init__(self, id):
        self.id = id    # id of the cell
        self.npcs = []  # characters in the cell
        self.items = [] # items in the cell

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
    print(m)

main()
