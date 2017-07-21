import pygame
import glb

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


        if "STOP_MOVE" not in actions :
            if dx > 0 :
                self.direction = glb.DIRECTION_RIGHT
            elif dx < 0 :
                self.direction = glb.DIRECTION_LEFT
            elif dy > 0 :
                self.direction = glb.DIRECTION_DOWN
            elif dy < 0 :
                self.direction = glb.DIRECTION_UP
            self.pos = next_pos








    def render(self):
        super().render( self.direction)

    def on_collision(self,you):
        if you.etype == glb.ETYPE_WALL:
            return "STOP_MOVE"
        elif you.etype == glb.ETYPE_DOOR:
            return self. on_door_collision(you)
        return None

    def on_door_collision(self,door):
        return "STOP_MOVE"



class Monster (Movable):
    def __init__(self,pos,etype,speed,direction, room_id ):
        super().__init__(pos,etype,speed,direction)

        self.img_list.append("monster_up.png")
        self.img_list.append("monster_right.png")
        self.img_list.append("monster_down.png")
        self.img_list.append("monster_left.png")
        self.load_imgs()

        self.move_strategy = RandomMoveStragery()

        glb.monster_list.append(self)

    def next_step(self):
        return self.move_strategy.next_step()
class Hero(Movable):
    def __init__(self,pos,etype,speed,direction):
        super().__init__(pos,etype,speed,direction)
        self.hp = 10
        self.invincible = False
        self.invincible_restround =0

        self.img_list.append("hero_up.png")
        self.img_list.append("hero_right.png")
        self.img_list.append("hero_down.png")
        self.img_list.append("hero_left.png")
        self.load_imgs()

        glb.hero = self
#colliderect(rect_2)
    def move(self,dx,dy):
        super().move(dx,dy)


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
