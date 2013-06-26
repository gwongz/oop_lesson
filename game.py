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

GAME_WIDTH = 7
GAME_HEIGHT = 7

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

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = False

    # Make things happen when you interact with chest 
    def interact(self, player):
        GAME_BOARD.draw_msg("Congratulations! You move on to the next level!")
        clear_board()
        initialize_level_2()



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

        if self.IMAGE == "GreenGem":
            GAME_BOARD.draw_msg("This is a bad gem.")
            clear_board()
            initialize()
            # GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            # GAME_BOARD.set_el(0, 0, PLAYER)
            # print PLAYER.x, PLAYER.y
        else: 
            player.inventory.append(self)
            GAME_BOARD.draw_msg("You just acquired a gem! You have %d gems!" % (len(player.inventory)))

            if len(player.inventory) == 5:
                # Initialize first object "chest" of class "Chest" and set it on GAME_BOARD
                chest = Chest()
                GAME_BOARD.register(chest)
                GAME_BOARD.set_el(5, 5, chest)
        

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        # door.SOLID = False

        GAME_BOARD.draw_msg("THIS KEY IS ALL YOU NEED!!!!!!111!!!!")

class Princess(GameElement):
    IMAGE = "Princess"
    SOLID = True

class Rock(GameElement): 
    IMAGE = "Rock"
    SOLID = True

class Wall(GameElement):
    IMAGE = "Wall"
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

    # Register good gems
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3,1,gem)

    gem2 = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(4,4, gem)

    gem3 = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(1,6,gem)

    gem4 = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(0,5,gem)

    # Register bad gem
    green_gem = Gem()
    green_gem.IMAGE = "GreenGem"
    GAME_BOARD.register(green_gem)
    GAME_BOARD.set_el(2, 3, green_gem)

    # Register key
    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(3, 3, key)


def initialize_level_2():

    # Adds chest and princess on empty game board at start of level 2
    chest_2 = Chest()
    GAME_BOARD.register(chest_2)
    GAME_BOARD.set_el(4, 3, chest_2)

    princess = Princess()
    GAME_BOARD.register(princess)
    GAME_BOARD.set_el(5, 3, princess)

    wall = Wall()
    GAME_BOARD.register(wall)
    GAME_BOARD.set_el(6, 3, wall)

def keyboard_handler():
    direction = None

    # Determines what direction the user wants to go in, based on the keyboard input
    if KEYBOARD[key.UP]:
        direction = "up"
    if KEYBOARD[key.DOWN]:
        direction = "down"
    if KEYBOARD[key.LEFT]:
        direction = "left"
    if KEYBOARD[key.RIGHT]:
        direction = "right"

    # If they press an arrow key
    if direction:
        # Determines location for character to move to based on direction
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        # If the next location is off the board, change the next location to be
        # at the opposite end of the board
        if next_x < 0:
            next_x = GAME_WIDTH - 1
        elif next_x > GAME_WIDTH - 1:
            next_x = 0
        elif next_y < 0:
            next_y = GAME_HEIGHT -1
        elif next_y > GAME_HEIGHT -1:
            next_y = 0
            

        # Checks what object (if any) is at the next location of the player
        existing_el = GAME_BOARD.get_el(next_x, next_y)

        # v v v This allows us to reset player to 0,0 after interacting with GreenGem or Chest 
        
        # If there is an existing object at the next location of the player,
        # and that object is either not a Green Gem, not a Chest, or not a Wall,
        # causes the player to interact with the existing object
        if existing_el and (existing_el.IMAGE != "GreenGem" or existing_el.IMAGE != "Chest" or existing_el.IMAGE != "Wall"):
            existing_el.interact(PLAYER)

        
        # If there is an existing object at the next location of the player,
        # and that object is a wall,
        if existing_el and existing_el.IMAGE == "Wall":
            # If the user wants to move the player up, and that position is on the board, it moves the player
            # to that location; but if that position is off the board, it resets the position to the opposite
            # end of the board. Then, if the next position of the WALL is 
            if direction == "up":
                if next_y - 1 < 0:
                    next_y_wall = GAME_HEIGHT - 1
                else:
                    next_y_wall = next_y - 1

                if not GAME_BOARD.get_el(next_x, next_y_wall):
                    GAME_BOARD.del_el(next_x, next_y)
                    GAME_BOARD.set_el(next_x, next_y_wall, existing_el)
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
            
            elif direction == "down":
                if next_y + 1 > GAME_HEIGHT - 1:
                    next_y_wall = 0
                else:
                    next_y_wall = next_y + 1

                if not GAME_BOARD.get_el(next_x, next_y_wall):
                    GAME_BOARD.del_el(next_x, next_y)
                    GAME_BOARD.set_el(next_x, next_y_wall, existing_el)
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
            
            elif direction == "right":
                if next_x + 1 > GAME_WIDTH - 1:
                    next_x_wall = 0
                else:
                    next_x_wall = next_x + 1

                if not GAME_BOARD.get_el(next_x_wall, next_y):
                    GAME_BOARD.del_el(next_x, next_y)
                    GAME_BOARD.set_el(next_x_wall, next_y, existing_el)
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)
            else:
                if next_x - 1 < 0:
                    next_x_wall = GAME_WIDTH - 1
                else:
                    next_x_wall = next_x - 1

                if not GAME_BOARD.get_el(next_x_wall, next_y):
                    GAME_BOARD.del_el(next_x, next_y)
                    GAME_BOARD.set_el(next_x_wall, next_y, existing_el)
                    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                    GAME_BOARD.set_el(next_x, next_y, PLAYER)

        if existing_el is None or not existing_el.SOLID:
            # If there's nothing there or if the existing element is 
            # not solid, or if the images is not a Wall,then walk through
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

        if existing_el and (existing_el.IMAGE == "GreenGem" or existing_el.IMAGE == "Chest"):
            existing_el.interact(PLAYER)

def clear_board():
    for x in range(GAME_WIDTH):
        for y in range(GAME_HEIGHT):
            if GAME_BOARD.get_el(x, y):
                GAME_BOARD.del_el(x, y)

    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
    GAME_BOARD.set_el(0, 0, PLAYER)