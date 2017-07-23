import pygame
import glb
import display

class Entity:
    #rect for collide and render
    #u,r,d,r
    def __init__(self,pos,etype):
        self.pos = pos
        self.img_list =[]
        self.etype = etype

        glb.entity_list.append(self)

    def load_imgs(self):
        for i,img_name in enumerate(self.img_list):
            self.img_list[i] = pygame.image.load(img_name)

    def render(self,img_idx=0):
         glb.screen.blit( self.img_list[img_idx ] ,self.get_rect() )

    def get_rect(self):
         rect = pygame.Rect(self.pos[0],self.pos[1],glb.W,glb.H)
         return rect
    #will call by each other .. only modified self preperty
    def on_collision(self,you):
        pass

class Goal(Entity):
     def __init__(self,pos):
        super().__init__(pos,glb.ETYPE_GOAL)
        self.img_list.append("goal.png")
        self.load_imgs()

        glb.goal = self

     def touched(self):
        glb.win()


class Wall(Entity):
    def __init__(self,pos):
        super().__init__(pos,glb.ETYPE_WALL)
        self.img_list.append("wall.png")
        self.load_imgs()

        glb.walls.append(self)

class Door(Entity):
    def __init__(self,pos,room_id):
        super().__init__(pos,glb.ETYPE_DOOR)
        self.img_list.append("door.png")
        self.load_imgs()

        self.room_id = room_id

        glb.door_list.append(self)

    def destroy(self):
        glb.door_list.remove(self)
        glb.entity_list.remove(self)


class Movable(Entity):
    def __init__(self,pos,etype,speed,direction):
        super().__init__(pos,etype)
        self.speed = speed
        self.direction = direction

        glb.movable_list.append(self)

    def get_collision_items(self,next_rect):
        l = []
        for et   in  glb.entity_list:
            if et == self:
                continue
            if et.get_rect().colliderect(next_rect):
                l.append(et)
        return l


    def move(self,dx,dy):
        next_pos = (self.pos[0]+dx,self.pos[1]+dy)
        next_rect =  pygame.Rect(self.pos[0]+dx,self.pos[1]+dy,glb.W,glb.H)

        l = self.get_collision_items(next_rect)
       # print(len(l))
        actions = {}
        for you in l:
            act = self.on_collision(you)
            if act is not None:
                actions[act] = True

        if dx > 0 :
            self.direction = glb.DIRECTION_RIGHT
        elif dx < 0 :
            self.direction = glb.DIRECTION_LEFT
        elif dy > 0 :
            self.direction = glb.DIRECTION_DOWN
        elif dy < 0 :
            self.direction = glb.DIRECTION_UP

        if "STOP_MOVE" not in actions :
            self.pos = next_pos

        self.move_event_handle()




    def render(self):
        super().render( self.direction)

    def on_collision(self,you):
        if you.etype == glb.ETYPE_WALL:
            return self. on_wall_collision(you)
        elif you.etype == glb.ETYPE_DOOR:
            return self. on_door_collision(you)
        elif you.etype == glb.ETYPE_MONSTER:
            return self. on_monster_collision(you)
        elif you.etype == glb.ETYPE_HERO:
            return self. on_hero_collision(you)
        elif you.etype == glb.ETYPE_FOOD:
            return self. on_food_collision(you)
        elif you.etype == glb.ETYPE_GOAL:
            return self. on_goal_collision(you)

    def on_goal_collision(self,goal):
        pass

    def on_wall_collision(self,wall):
        return  "STOP_MOVE"
    def on_door_collision(self,door):
        return "STOP_MOVE"
    def  on_monster_collision(self,monster):
        pass
    def on_hero_collision(self,hero):
        pass
    def on_food_collision(self,food):
        pass
    def move_event_handle(self):
        pass
class Monster (Movable):
    def __init__(self,pos,etype,speed,direction, room_id ):
        super().__init__(pos,etype,speed,direction)

        self.img_list.append("monster_up.png")
        self.img_list.append("monster_right.png")
        self.img_list.append("monster_down.png")
        self.img_list.append("monster_left.png")
        self.load_imgs()

        self.room_id = room_id
        self.move_strategy = RandomMoveStragery()

        glb.monster_list.append(self)

    def on_monster_collision(self,hero):
        self.move_strategy.reset()
        return "STOP_MOVE"

    def on_hero_collision(self,hero):
        self.move_strategy.reset()
        hero.change_hp(-1)
        return  "STOP_MOVE"

    def on_door_collision(self,door):
        self.move_strategy.reset()
        return  "STOP_MOVE"

    def on_wall_collision(self,wall):
        #print('124')
        self.move_strategy.reset()
        return  "STOP_MOVE"

    def next_step(self):
        return self.move_strategy.next_step()

    def dead(self):
        glb.monster_list.remove(self)
        glb.entity_list.remove(self)

class Hero(Movable):
    def __init__(self,pos,etype,speed,direction):
        super().__init__(pos,etype,speed,direction)
        self.hp = 10
        self.max_hp =  self.hp
        self.invincible = False
        self.invincible_restround =0

        self.img_list.append("hero_up.png")
        self.img_list.append("hero_right.png")
        self.img_list.append("hero_down.png")
        self.img_list.append("hero_left.png")
        self.load_imgs()
        #events
        self.monster_attackers = []
        self.food_pack     = []
        self.food_new = None
        self.current_room = 0

        glb.hero = self

    def goto_next_room(self):
        display.info_displayer.cls_info()
        display.info_displayer.info_nextline("you can go to next room %d"%(self.current_room+1) )

        display.wait_enter()


        display.info_displayer.cls_info()
        display.info_displayer.info_nextline("you can move now" )
        #

        self.current_room +=1

        glb.init_foods(self.current_room)
        glb.init_monsters(self.current_room)


    def on_door_collision(self,door):

        if len(self.food_pack) == 4 :
            #clear all door of current room
            for door in glb.door_list[:] :  #copy a list of door list because we delete item from this list
                                                        #while iterate it
                #print('door collision')
                #print(door.room_id)
                if door.room_id == self.current_room:
                    door.destroy()
            for monster  in glb.monster_list[:]:
                if monster.room_id == self.current_room:
                    monster.dead()
            self.food_pack = []

            self.goto_next_room()


        return "STOP_MOVE"


    def on_monster_collision(self,monster):
        # hp --
        if  monster not in self.monster_attackers:
            self.monster_attackers.append(monster)
        return "STOP_MOVE"

    def on_food_collision(self,food):
        self.food_new = food

    def on_goal_collision(self,goal):
        goal.touched()

    def  change_hp(self,delta):
        self.hp += delta
        if self.hp <= 0:
            self.hp = 0
            self.dead()

        elif self.hp > self.max_hp:
            self.hp = 10

    def move_event_handle(self):
        #handle hp --
        attack_times = len(self.monster_attackers)
        self.change_hp(-1*attack_times)

        if self.food_new is not None:
            can_eat_food = True
            print('eat check')
            for monster in self.monster_attackers:
                if monster.get_rect().colliderect(self.food_new.get_rect() ):
                    can_eat_food = False
            if can_eat_food:
                self.food_pack.append(self.food_new)
                print('eat a new food : food len = %d'%(len(self.food_pack) ) )
                self.food_new.eaten()



        self.monster_attackers = []
        self.food_new = None

    def dead(self):
        display.info_displayer.cls_info()
        display.info_displayer.info_nextline("you dead !!" )
        display.info_displayer.info_nextline("Hero relives")
        glb.render_all()
        display.wait_enter()
        display.info_displayer.cls_info()
        display.info_displayer.info_nextline("you relives and must go over all rooms again")
        glb.hero = None

        glb.init_game_entities()


class Food(Entity):
    def __init__(self,pos,room_id):
        super().__init__(pos,glb.ETYPE_FOOD)
        self.img_list.append("food.png")
        self.load_imgs()
        self.room_id = room_id

        glb.food_list.append(self)

    def eaten(self):
        glb.food_list.remove(self)
        glb.entity_list.remove(self)

import random
class RandomMoveStragery:
    #0. if rest_step is 0
        #1. generate a direction
        #2. generate a step 1~3 randomly
    #rest_step --
    def __init__(self):
        self.rest_step = 0
        self.dx = 0
        self.dy = 0

    def reset(self):
        self.rest_step = 0
    def next_step(self):

        if self.rest_step > 0 :
            pass
        else :
            self.rest_step = random.randint(1,3)
            # up,right,down,left ,stop
            flag = random.randint(0,4)
            if flag == 0:
                self.dx = 0
                self.dy = 0
                self.rest_step = 1
            elif flag == 1:
                self.dx = 0
                self.dy = -1
            elif flag == 2:
                self.dx = 1
                self.dy = 0
            elif flag == 3:
                self.dx = 0
                self.dy = 1
            elif flag == 4:
                self.dx = -1
                self.dy = 0
            self.dx,self.dy =  self.dx*glb.W , self.dy*glb.H

        self.rest_step-=1

        #print((self.dx,self.dy))
        return self.dx,self.dy
