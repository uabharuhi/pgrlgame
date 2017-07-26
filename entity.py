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

    def get_collision_items(self,next_rect):
        l = []
        for et   in  glb.entity_list:
            if et == self:
                continue
            if et.get_rect().colliderect(next_rect):
                l.append(et)
        return l

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

        self.hp = 6
        self.room_id = room_id
        self.move_strategy = RandomMoveStragery()

        glb.monster_list.append(self)

    def decrease_hp(self,n):
        print('??')
        if self.hp>0:
            self.hp-=n
        if self.hp <=0:
            self.hp = 0
            self.dead()

    def on_monster_collision(self,hero):
        self.move_strategy.reset()
        return "STOP_MOVE"

    def on_hero_collision(self,hero):
        self.move_strategy.reset()
        hero.change_hp(-1)
        print(glb.hero.hp)
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
    def __init__(self,pos,speed,direction):
        etype = glb.ETYPE_HERO
        super().__init__(pos,etype,speed,direction)
        self.hp = 1000
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

        self.current_cd = 0

        glb.hero = self

    def goto_next_room(self):
        display.info_displayer.cls_info()
        display.info_displayer.info_nextline("you can go to next room %d"%(self.current_room+1) )

        display.wait_enter()


        display.info_displayer.cls_info()
        display.info_displayer.info_nextline("you can move now" )
        #

        self.current_room +=1

        glb.init_room(self.current_room)
       

    def on_door_collision(self,door):

        if len(glb.monster_list) == 0  :
            #clear all door of current room
            for door in glb.door_list[:] :  #copy a list of door list because we delete item from this list
                if door.room_id == self.current_room:
                    door.destroy()

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


    def decrease_cd(self):
        if self.current_cd>0:
            self.current_cd-=1

class SwordAttack(Entity):
    def __init__(self,pos,direction,attacker):
        super().__init__(pos,glb.ETYPE_ATTACK)
        self.img_list.append("sword_up.png")
        self.img_list.append("sword_right.png")
        self.img_list.append("sword_down.png")
        self.img_list.append("sword_left.png")
        self.load_imgs()
        self.direction = direction
        self.attacker = attacker
        self.damage = 3

    def fire(self):
        l = self.get_collision_items(self.get_rect())
        for e in l:
            if e.etype == glb.ETYPE_MONSTER:
                self.attacker.hp+=1
                e.decrease_hp(self.damage)

    def render(self):
       # print('1234')
        super().render( self.direction)
    def get_rect(self):
        if self.direction == glb.DIRECTION_DOWN or self.direction == glb.DIRECTION_UP:
            rect = pygame.Rect(self.pos[0],self.pos[1],glb.W,3*glb.H)
        else:
            rect = pygame.Rect(self.pos[0],self.pos[1],3*glb.W,glb.H)
        return rect
    def destroy(self):
        glb.entity_list.remove(self)

        #if self.rest_round == 0:
        #    self.attacker. is_attacking =False
        #else:
        #    self.attacker.is_attacking = True


class Kirito(Hero):
        def __init__(self,pos,speed,direction):
            super().__init__(pos,speed,direction)
            self.attack_obj = None
            self.attack_cd = 4
            self.hp = 10

        def attack(self):
            if  self.current_cd > 0 :
                return

            elapsed_count = 3
            #                   up,right,down
            rect = self.get_rect()
            rect1 = rect.move(0,-3*glb.H)
            rect2 = rect.move(glb.W,0)
            rect3 = rect.move(0,1*glb.H)
            rect4 = rect.move(-3*glb.W,0)
            attack_order_list = [rect1,rect2,rect3,rect4]
            attack_idx = self.direction-1

            if attack_idx<0:
                attack_idx = 3
            #start of idx
            sword = None

            while elapsed_count>0:
                glb.clock.tick(20)

               # pygame.time.delay(2500)
                #if sword is not None:
                    #sword.destroy()
                #print(attack_idx)
                next_rect = attack_order_list[attack_idx]
                sword = SwordAttack((next_rect.x,next_rect.y),attack_idx,self)
                sword.fire()
                elapsed_count-=1
                print('s %d'%sword.direction)
                glb.screen.fill((0, 0, 0),pygame.Rect(0,0,400,400))
                sword.render()
                glb.render_all()

               #pygame.display.flip()

                attack_idx+=1
                if attack_idx>3:
                    attack_idx = 0

          
            glb.clock.tick(4)
            glb.screen.fill((0, 0, 0),pygame.Rect(0,0,400,400))
            glb.render_all()
            self.current_cd =  self.attack_cd


class Explosion(Movable):

    def __init__(self,pos,speed,direction):
         super().__init__(pos,glb.ETYPE_ATTACK,speed,direction)
         glb.attack_list.append(self)
         self.destroyed = False

         if not self.in_boundary():
            self.destroy()
            #print('aa')
         self.img_list.append("explosion.png")
         self.img_list.append("explosion.png")
         self.img_list.append("explosion.png")
         self.img_list.append("explosion.png")
         self.load_imgs()

         #handle the condition move function destroyed twice
         self.time = 5
         self.damage = 2


    def move(self,dx,dy):
        next_pos = (self.pos[0]+dx,self.pos[1]+dy)
        next_rect =  pygame.Rect(self.pos[0]+dx,self.pos[1]+dy,glb.W,glb.H)


        l = self.get_collision_items(next_rect)
        for you in l:
            self.on_collision(you)
        self.pos = next_pos
        self.time-=1
        if not self.in_boundary() or self.time<=0:
            self.destroy()


    def in_boundary(self):
        x,y = self.pos[0],self.pos[1]
        if x >= 380 or y>=380 or y<20 or x<20 :
            return False
        return True
    def next_step(self):
        dx,dy = 0,0
        if self.direction == glb.DIRECTION_UP:
            dy = -1*self.speed
        elif self.direction == glb.DIRECTION_RIGHT:
            dx =  self.speed
        elif self.direction == glb.DIRECTION_DOWN:
            dy = self.speed
        elif self.direction == glb.DIRECTION_LEFT:
            dx =  -1*self.speed
        return dx,dy

    def on_monster_collision(self,you):
        self.destroy()
        you.decrease_hp(self.damage)

  
        #self.de

    def destroy(self):
        if not self.destroyed :
            glb.movable_list.remove(self)
            glb.entity_list.remove(self)
            glb.attack_list.remove(self)
            self.destroyed = True






class Megumi(Hero):

        def attack(self):
            self.attack_cd = 6
            self.create_explosions()


        def create_explosions(self):
            if self.current_cd >0:
                return 
            w,h = glb.W,glb.H
            x,y = self.pos[0],self.pos[1]
            if self.direction == glb.DIRECTION_UP:
                pos_list = [(x,y),(x-w,y),(x+w,y),(x,y-h)]
            elif self.direction == glb.DIRECTION_RIGHT:
                pos_list = [(x,y),(x,y+h),(x,y-h),(x+w,y)]
            elif self.direction == glb.DIRECTION_DOWN:
                pos_list = [(x,y),(x-w,y),(x+w,y),(x,y+h)]
            elif self.direction == glb.DIRECTION_LEFT:
                pos_list = [(x,y),(x-w,y),(x,y-h),(x,y+h)]
            ex_list = []
            for pos in pos_list:
                #glb.W+10 :speed sightly faster than normal speed
                ex = Explosion(pos,glb.W+10,self.direction)
                ex_list.append(ex)
            self.current_cd =  self.attack_cd



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
