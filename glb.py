# this file contains all global object
import entity
import pygame

screen = None
walls = None
doors = None
clock = None
hero = None
entity_list  = []
W = 20
H = 20
ETYPE_WALL = 0
ETYPE_DOOR = 1
ETYPE_HERO = 2

DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3

level = [
#123456789012345678901234567890
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W        WW        WW        W",
"W        WW        WW        W",
"W        WW        WW        W",
"W        11        22        W",
#- - -- - - - -- - - - - -
"W        11        22        W",
"W        WW        WW        W",
"W        WW        WW        W",
"W        WW        WW        W",
"WWWWWWWWWWWWWWWWWWWWWWWW33WWWW",
"WWWWWWWWWWWWWWWWWWWWWWWW33WWWW",
"W        WW        WW        W",
"W        WW        WW        W",
"W        WW        WW        W",
"W        55        44        W",
#- - -- - - - -- - - - - -
"W        55        44        W",
"W        WW        WW        W",
"W        WW        WW        W",
"W        WW        WW        W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
]


def init_game():
    global screen,walls,doors,clock
    pygame.init()
    # Set up the display
    pygame.display.set_caption("test")
    #pygame.key.set_repeat(10,10)
    #                                 width ,height
    screen = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()
    walls = [] # List to hold the walls
    doors = []

    hero = entity.Hero((40,40),ETYPE_HERO,W,DIRECTION_RIGHT)



    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                entity.Wall((x, y))
            if col.isdigit():
                room_id = int(col)
                entity.Door((x,y),room_id)
            x += W
        y += H
        x = 0
    pygame.display.flip()
    #player = Player() # Create the player

def render_all():
    hero.render()
    for wall in walls:
        wall.render()
    pygame.display.flip()