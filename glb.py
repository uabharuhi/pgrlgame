# this file contains all global object
import entity
import pygame

screen = None
clock = None
hero = None
W = 20
H = 20
ETYPE_WALL = 0
ETYPE_DOOR = 1
ETYPE_HERO = 2
ETYPE_MONSTER = 3
ETYPE_FOOD= 4

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

walls = []
entity_list = []
movable_list = []
door_list = []
monster_list = []
food_list = []

def init_game():
    global screen,walls,doors,clock
    pygame.init()
    # Set up the display
    pygame.display.set_caption("test")
    #pygame.key.set_repeat(10,10)
    #                                 width ,height
    screen = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

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


    entity.Hero((40,40),ETYPE_HERO,W,DIRECTION_RIGHT)
    init_monsters()
    init_foods()
    pygame.display.flip()

    #player = Player() # Create the player

def init_foods():
    init_info = [ ((20,20),0)  ,((20,160),0) , ((160,20),0) , ((160,160),0) ]
    for info in init_info:
        entity.Food(info[0] , info[1])


def init_monsters():
    init_info = [ ((160,100),0)  ]

    for info in init_info:
        entity.Monster(info[0], ETYPE_MONSTER , W , DIRECTION_LEFT , info[1])





def render_all():

    for wall in walls:
        wall.render()
    for door in door_list:
        door.render()
    for food in food_list:
        food.render()
    hero. render()

    for monster in monster_list:
        monster.render()


    pygame.display.flip()
