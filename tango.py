from bot import Bot
from client import Client

# Tango defines the behavior of a Tango bot
class Tango:
    # ports with which to access servos on the robot
    WAIST = 0
    SAME = 1 # wheels spinning in the same direction
    DIFF = 2 # wheels spinning in the opposite direction
    SIDE = 3 # head moving side-to-side
    UPDOWN = 4 # head moving up/down

    LEFT_SHOULDER = 12

    CENTER = 6000 # where the Tango bot's joints are centered and speed is at 0
    TO_EXT = 3000 # the farthest from self.CENTER the joints and speed can go

    def __init__(self):
        self.tango = Bot() # bot instance for Tango bot

    # center brings the given joint back to center
    def center(self, port):
        self.tango.bendTurn(port, self.CENTER)

    # drive allows the tango bot to drive forwards or backwards at 3 different speeds
    def drive(self, direction):
        pos = self.tango.position(self.SAME) # determine the wheels' current position
        inc = self.TO_EXT // 3 # accelerate with 3 speeds

        # backward direction
        if direction == False:
            # negatively accelerate the tango bot as long as it is not moving at its' maximum backward speed
            if pos < self.CENTER + self.TO_EXT:
                self.tango.accelerate(self.SAME, pos + inc, .0005)
        # forward direction
        elif direction == True:
            # positively accelerate the tango bot as long as it is not moving at its' maximum forward speed
            if pos > self.CENTER - self.TO_EXT:
                self.tango.accelerate(self.SAME, pos - inc, .0005)

    # head allows the Tango bot's head to turn or tilt with 5 degrees of resolution
    def head(self, direction, port):
        pos = self.tango.position(port) # determine the head's current position on the desired axis
        inc = self.TO_EXT // 5 # turn on 5 degrees/steps of resolution

        # tilt the head down / turn it right
        if direction == False:
            if pos > self.CENTER - self.TO_EXT:
                self.tango.bendTurn(port, pos - inc)
        # tilt the head up / turn it left
        elif direction == True:
            if pos < self.CENTER + self.TO_EXT:
                self.tango.bendTurn(port, pos + inc)

    # reset sets all joints and wheel speeds to their central setting
    def reset(self):
        self.stop()
        self.center(self.WAIST)
        self.center(self.SIDE)
        self.center(self.UPDOWN)
        self.tango.head(False, Tango.LEFT_SHOULDER)
        self.tango.head(False, Tango.LEFT_SHOULDER)
        self.tango.head(False, Tango.LEFT_SHOULDER)
        self.tango.head(False, Tango.LEFT_SHOULDER)
        self.tango.head(False, Tango.LEFT_SHOULDER)

    def speak(self, phrase):
        ''' speak sends the given message to Android to convert to speech '''
        Client.sendMessage('<speak> ' + phrase)

    # stop brings a moving Tango bot to a stop
    def stop(self):
        self.tango.accelerate(self.DIFF, self.CENTER, 0)
        self.tango.accelerate(self.SAME, self.CENTER, .0005)

    # turn allows the Tango bot to turn left or right
    def turn(self, direction):
        pos = self.tango.position(self.DIFF) # determine the wheels' current position
        inc = self.TO_EXT // 3 # accelerate with 3 speeds

        # left turn
        if direction == False:
            # accelerate the wheels (L:-, R:0), leading to a left turn
            if pos < self.CENTER + self.TO_EXT:
                self.tango.accelerate(self.DIFF, pos + inc, 0)
        # right direction
        elif direction == True:
            # accelerate the wheels (L:0, R:-), leading to a right turn
            if pos > self.CENTER - self.TO_EXT:
                self.tango.accelerate(self.DIFF, pos - inc, 0)

    # twist allows the Tango bot to twist at the waist along 3 degrees of resolution
    def twist(self, direction):
        pos = self.tango.position(self.WAIST) # determine the waist's current position
        inc = self.TO_EXT // 3 # twist on 3 degrees of resolution

        # twist left
        if direction == False:
            if pos < self.CENTER + self.TO_EXT:
                self.tango.bendTurn(self.WAIST, pos + inc)
        # twist right
        elif direction == True:
            if pos > self.CENTER - self.TO_EXT:
                self.tango.bendTurn(self.WAIST, pos - inc)
