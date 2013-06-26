import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
#######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####



class Character(GameElement):
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    IMAGE = "Girl"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Boy(Character):
    def __init__(self):  
        Character.__init__(self)

    IMAGE = "Boy"
    SOLID = True 

    def interact(self, player):
        GAME_BOARD.draw_msg("Hey, girl. There is a bad gem on the board.")

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        for item in player.inventory:
            if item.IMAGE == "Key":
                door.SOLID = False
                break

class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False 

    def interact(self, player):
        player.inventory.append(self)

        if self.IMAGE == "GreenGem":
            GAME_BOARD.draw_msg("This is a bad gem.")
            # GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            # GAME_BOARD.set_el(0, 0, PLAYER)
            # print PLAYER.x, PLAYER.y
        
        else: 
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        # door.SOLID = False

        GAME_BOARD.draw_msg("THIS KEY IS ALL YOU NEED!!!!!!111!!!!")

class Rock(GameElement): 
    IMAGE = "Rock"
    SOLID = True

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    rock_positions = [(4, 0), (4, 1), (4, 2), (3, 0), (2, 0), (2, 1), (2, 2)]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    for rock in rocks:
        print rock

    # Register boy
    boy = Boy()
    GAME_BOARD.register(boy)
    GAME_BOARD.set_el(1,3, boy)

    # Register character
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 0, PLAYER)
    print PLAYER

    # Display message on screen
    GAME_BOARD.draw_msg("This game is wicked awesome.")

    # Register door
    global door 
    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(3,2,door)

    # Register gems
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3,1,gem)

    green_gem = Gem()
    green_gem.IMAGE = "GreenGem"
    GAME_BOARD.register(green_gem)
    GAME_BOARD.set_el(2, 3, green_gem)

    # Register key
    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(3, 3, key)


def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if next_x < 0:
            next_x = GAME_WIDTH - 1
        elif next_x > GAME_WIDTH - 1:
            next_x = 0
        elif next_y < 0:
            next_y = GAME_HEIGHT -1
        elif next_y > GAME_HEIGHT -1:
            next_y = 0
            

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el:
            existing_el.interact(PLAYER)

        if existing_el is None or not existing_el.SOLID:
            # If there's nothing there or if the existing element is 
            # not solid, walk through
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

