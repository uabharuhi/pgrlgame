import pygame
import glb

class Entity:
    #rect for collide and render
    #u,r,d,r
    def __init__(self,pos,etype):
        self.pos = pos
        self.img_list =[]
        self.etype = etype
        self.rect = pygame.Rect(self.pos[0],self.pos[1],glb.W,glb.H)

        self.lookahead_pos = self.pos
        self.lookahead_rect = self.rect 
        self.overlapable = False # for collide
        self.action_dict = {}

        glb.entity_list.append(self)


    def load_imgs(self):
        for i,img_name in enumerate(self.img_list):
            self.img_list[i] = pygame.image.load(img_name)

    def render(self,img_idx=0):
        self.render_rect(self.img_list[img_idx])

    def render_rect(self,img):
        glb.screen.blit(img,self.rect)



    def collide(self,you):
        pass

    def take_actions(self):
        pass

    def check_all_collision(self):
        victim_list = self.detect_collide_objects()
        for you in victim_list:
            if you.etype == glb.ETYPE_WALL:
                self.action_dict["STOP_MOVE"] = True
        return victim_list

    def check_collision(self,you):
        #self x,y,w,h
        self_x1,self_x2 = min(self.pos[0],self.lookahead_pos[0]),max(self.pos[0],self.lookahead_pos[0])
        self_y1,self_y2 = min(self.pos[1],self.lookahead_pos[1]),max(self.pos[1],self.lookahead_pos[1])
        rect_1 = pygame.Rect(self_x1,self_y1,self_x2-self_x1+glb.W,self_y2-self_y1+glb.H)

        you_x1,you_x2 = min(you.pos[0],you.lookahead_pos[0]),max(you.pos[0],you.lookahead_pos[0])
        you_y1,you_y2 = min(you.pos[1],you.lookahead_pos[1]),max(you.pos[1],you.lookahead_pos[1])
        rect_2 = pygame.Rect(you_x1,you_y1,you_x2-you_x1+glb.W,you_y2-you_y1+glb.H)
        #if self == glb.hero :
        #    print("rect1")
        #    print(rect_1)
        #    print("rect2")
        #    print(rect_2)

        if self.lookahead_rect.colliderect(rect_2) and you.lookahead_rect.colliderect(rect_1):
            return True
        return False

    def detect_collide_objects(self):
        l = []
        for et   in  glb.entity_list:
            if et == self:
                continue
            if self.check_collision(et):
                l.append(et)
        return l

    def set_current_pos(self,pos):
        x,y = pos[0],pos[1]
        self.pos = (x,y)
        self.rect = pygame.Rect(x,y,glb.W,glb.H)
        self.lookahead_pos = self.pos
        self.lookahead_rect= self.rect
    #



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

        glb.doors.append(self)

class Movable(Entity):
    def __init__(self,pos,etype,speed,direction):
        super().__init__(pos,etype)
        self.speed = speed
        self.direction = direction


    def collide(self,you):
        pass

    #for collision,before move call this function to get next_pos

    def lookahead(self,dx,dy):
        self.lookahead_pos = (self.pos[0]+dx,self.pos[1]+dy)
        self.lookahead_rect =  pygame.Rect(self.pos[0]+dx,self.pos[1]+dy,glb.W,glb.H)

        #print(self.lookahead_rect )


    def take_actions(self):
        if "STOP_MOVE" in self.action_dict:
    
            self.set_current_pos(self.pos)
        else :
            dx = self.lookahead_pos[0] - self.pos[0]
            dy = self.lookahead_pos[1] - self.pos[1]

            if  dx > 0 :
                self.direction = glb.DIRECTION_RIGHT
            elif dx < 0 :
                self.direction = glb.DIRECTION_LEFT
            elif dy > 0 :
                self.direction = glb.DIRECTION_DOWN
            elif dy < 0 :
                self.direction = glb.DIRECTION_UP

        self.set_current_pos(self.lookahead_pos)
        

    def render(self):
        super().render_rect( self.img_list[self.direction] )

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


    def take_actions(self):
        super().take_actions()
        self.action_dict = {} 

    def check_all_collision(self):
        l = super().check_all_collision()
        for you in l :
            if you.etype == glb.ETYPE_DOOR:
                self.action_dict["STOP_MOVE"] = True

class Monster(Movable):
    def __init__(self,pos,etype,speed,direction):
        super().__init__(pos,etype,speed,direction)

        self.img_list.append("monster_up.png")
        self.img_list.append("monster_right.png")
        self.img_list.append("monster_down.png")
        self.img_list.append("monster_left.png")
        self.load_imgs() 

        glb.monster_list.append(self)