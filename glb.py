# this file contains all global object
import entity
import pygame
import display

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
                room_id = int(col) -1
                entity.Door((x,y),room_id)
            x += W
        y += H
        x = 0
    #for door in door_list:
        #print(door.room_id)

    entity.Hero((40,40),ETYPE_HERO,W,DIRECTION_RIGHT)
    init_monsters(0)
    init_foods(0)

    display.info_displayer.show_info("Welcome!")
    display.info_displayer.info_nextline("Move your hero to eat 4 foods at corner in each room")
    display.info_displayer.info_nextline("Be careful to monster, hero's hp will decrease if touch by monsters !!")

    pygame.display.flip()

    #player = Player() # Create the player

def init_foods(room_id):
    init_info = [ ((20,20),0)  ,((20,160),0) , ((160,20),0) , ((160,160),0), #0
                    ((220,20),1)  ,((220,160),1) , ((360,20),1) , ((360,160),1)  #1
                    ]
    for pos,rid in init_info:
        if  rid == room_id:
            entity.Food(pos ,rid )


def init_monsters(room_id):
    init_info = [ ((160,100),0),((360,40),1),((360,140),1)  ]

    for pos,rid in init_info:
        if rid == room_id:
            entity.Monster(pos, ETYPE_MONSTER , W , DIRECTION_LEFT , rid)

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

    display.state_displayer.show_hero_state()


    pygame.display.flip()
