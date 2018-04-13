from map import Map

class Adventure:
    def __init__(self, map_file_name, create_character):
        self.player = None
        self.world = Map(map_file_name) # load the given map as the world for the adventure
        if create_character:
            self.create_character()

    def create_character(self):
        return

    def start(self):
        ''' start kicks off an adventure '''
        print(self.world)

def main():
    adv = Adventure('map1.txt', False)
    adv.start()
main()
