# this file contains all global object
import entity
import pygame

W = 20
H = 20

screen = None
walls = None
doors = None
clock = None
hero = None
monster = None

current_room = 0
#monster_init_pos[current_room_id] --> list of pos of monter
monster_room_pos = [  [ (8*W,4*H) ] ]

entity_list  = []
monster_list=  []
ETYPE_WALL = 0
ETYPE_DOOR = 1
ETYPE_HERO = 2
ETYPE_MONSTER = 2

DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3





monster_init_pos = []

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
    #create hero
    entity.Hero((40,40),ETYPE_HERO,W,DIRECTION_RIGHT)
    #create monster
    for m_pos in monster_room_pos[0] :
        entity.Monster(m_pos,ETYPE_MONSTER,W,DIRECTION_LEFT,entity.RandomMoveStragery())

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
   

def render_all():
    for et in entity_list:
        et.render()
    pygame.display.flip()