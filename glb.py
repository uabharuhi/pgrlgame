# this file contains all global object
import entity
import pygame
import display


test_mode = True
test_room = 0

running = True
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
ETYPE_GOAL= 5

DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3

level = [
#123456789012345678901234567890
"WWWWWWWWWWWWWWWWWWWW",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
#- - -- - - - -- - - - - -
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"W                  D",
"W                  D",
"W                  W",
"W                  W",
"W                  W",
"W                  W",
#- - -- - - - -- - - - - -
"W                  W",
"W                  W",
"W                  W",
"W                  W",
"WWWWWWWWWWWWWWWWWWWW"
]

walls = []
entity_list = [] #for collision check
movable_list = []
door_list = []
monster_list = []
food_list = []



def init_room(room_id,hero_pos=(40,200)):
    global  walls,movable_list,door_list ,monster_list ,food_list

    walls = []
    door_list = []
    monster_list = []
    food_list = []

    init_wall_and_door(room_id)

    hero.pos = hero_pos

    init_monsters(room_id)


def init_wall_and_door(room_id):
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                entity.Wall((x, y))
            if col=="D":
                entity.Door((x,y),room_id)
            x += W
        y += H
        x = 0

def init_game():
    global screen,walls,doors,clock,hero

    pygame.init()
    pygame.display.set_caption("test")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    # pos will after set by init_room
    hero  = entity.Hero((0,0),W,DIRECTION_RIGHT)

    if test_mode:
        hero.current_room = test_room
    if test_mode:
        init_room(test_room)
    else:
        init_room(0)


    #display.info_displayer.show_info("Welcome!")
    #display.info_displayer.info_nextline("Move your hero to eat 4 foods at corner in each room")
    #display.info_displayer.info_nextline("Be careful to monster, hero's hp will decrease if touch by monsters !!")

    pygame.display.flip()

#def init_hero_and_room():
#    global hero
#    hero = entity.Hero((40,40),W,DIRECTION_RIGHT)
#
#    if test_mode:
#        hero_pos = {0:(40,40),1:(240,40),2:(440,40),3:(440,240),4:(240,240),5:(40,240)}
#        hero.current_room = test_room
#        hero.pos = hero_pos[test_room]
#
#        init_monsters(test_room)
#        init_foods(test_room)
#    else:
#        init_monsters(0)
#        init_foods(0)
#

def init_foods(room_id):
    init_info = [ ((20,20),0)  ,((20,160),0) , ((160,20),0) , ((160,160),0), #0
                    ((220,20),1)  ,((220,160),1) , ((360,20),1) , ((360,160),1) , #1
                    ((420,20),2)  ,((420,160),2) , ((560,20),2) , ((560,160),2), # 2
                    ((420,220),3)  ,((420,360),3) , ((560,220),3) , ((560,360),3), # 3
                     ((220,220),4)  ,((220,360),4) , ((360,220),4) , ((360,360),4), # 4
                     #((20,220),5)  ,((20,360),5) , ((160,220),5) , ((160,360),5) # 5

                    ]
    for pos,rid in init_info:
        if  rid == room_id:
            entity.Food(pos ,rid )


def init_monsters(room_id):
    init_info = [ ((360 ,40),0),((360,120),0),((360,200),0),((360,280),0),((280,40),1),((280,120),1),
                     ((560,40),2),((560,140),2),((420,40),2) ,
                     ((560,240),3),((560,340),3),((420,240),3) ,
                     ((360,240),4),((360,340),4),((220,240),4)
     ]

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

    #display.state_displayer.show_hero_state()

    pygame.display.flip()

def win():
    global running
    display.info_displayer.cls_info()
    display.info_displayer.info_nextline("you win!!!!" )
    display.wait_enter()
    running   = False



