from tango import Tango
import time

class Playerbot:
    # changes to a 'current' location to go a specific direction TODO: these are copies from adventure; instead, break into a separate 'cardinal' file
    NORTH = [0, -1]
    EAST = [1, 0]
    SOUTH = [0, 1]
    WEST = [-1, 0]

    def __init__(self):
        self.tango = Tango() # the robot that will interact with the player
        self.cur_dir = Playerbot.NORTH # always start facing north
        self.tango.reset()

    def same_dir(dir1, dir2):
        for i, n in enumerate(dir1):
            if not (n == dir2[i]):
                return False
        return True

    def add_dir(dir1, dir2):
        ''' adds dir2 to dir1 '''
        result = []
        result.append(dir1[0]+dir2[0])
        result.append(dir1[1]+dir2[1])
        return result

    def diff_dir(dir1, dir2):
        ''' subtracts dir2 from dir1 '''
        result = []
        result.append(dir1[0]-dir2[0])
        result.append(dir1[1]-dir2[1])
        return result

    def encounter(self):
        ''' encounter makes tango look around like it has encountered an enemy '''
        self.tango.head(True, Tango.SIDE)
        self.tango.head(True, Tango.SIDE)
        time.sleep(.5)
        self.tango.head(False, Tango.SIDE)
        self.tango.head(False, Tango.SIDE)
        time.sleep(.25)
        self.tango.head(False, Tango.SIDE)
        self.tango.head(False, Tango.SIDE)
        time.sleep(.5)
        self.tango.head(True, Tango.SIDE)
        self.tango.head(True, Tango.SIDE)

    def hit(self):
        ''' hit makes the tango simulate dealing combat damage '''
        self.tango.twist(True)
        self.tango.twist(True)
        time.sleep(.25)
        self.tango.twist(False)
        self.tango.twist(False)

    def move(self, direction):
        ''' move makes tango drive in the given direction '''
        self.turn(direction)

        # move forward for 1s then stop
        self.tango.drive(True)
        time.sleep(.5)
        self.tango.stop()

    def turn(self, direction):
        ''' turn causes the tango to turn towards the given direction '''
        while not Playerbot.same_dir(self.cur_dir, direction):
            self.turn_90(direction)
        self.cur_dir = direction

    def turn_90(self, direction):
        ''' turn 90 makes a turn in 90 degree increments '''
        change = Playerbot.diff_dir(direction, self.cur_dir) # determine the change Tango must make to face the correct direction
        turn_dir = 0                                         # direction to turn (-1 for left, 1 for right)

        # based on the
        if Playerbot.same_dir(self.cur_dir, Playerbot.NORTH) or Playerbot.same_dir(self.cur_dir, Playerbot.SOUTH):
            if change[1] == 2:
                change[0] = 1
                change[1] = 1
            elif change[1] == -2:
                change[0] = -1
                change[1] = -1
            turn_dir = change[0]

            if Playerbot.same_dir(self.cur_dir, Playerbot.SOUTH):
                turn_dir = -turn_dir
        elif Playerbot.same_dir(self.cur_dir, Playerbot.EAST) or Playerbot.same_dir(self.cur_dir, Playerbot.WEST):
            if change[0] == 2:
                change[1] = 1
                change[0] = 1
            elif change[0] == -2:
                change[1] = -1
                change[0] = -1
            turn_dir = change[1]

            if Playerbot.same_dir(self.cur_dir, Playerbot.WEST):
                turn_dir = -turn_dir
        else:
            print("ERROR:", direction, "does not match an expected direction")

        if turn_dir < 0:
            turn_dir = False
        elif turn_dir > 0:
            turn_dir = True
        else:
            print("ERROR:", turn_dir, "does not imply a direction for turning")

        self.tango.turn(turn_dir)
        time.sleep(1.6)
        self.tango.stop()
        self.cur_dir = Playerbot.add_dir(change, self.cur_dir)
