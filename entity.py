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

    def load_imgs(self):
        for i,img_name in enumerate(self.img_list):
            self.img_list[i] = pygame.image.load(img_name)

    def render(self,img_idx=0):
        self.render_rect(self.img_list[img_idx])

    def render_rect(self,img):
        glb.screen.blit(img,self.rect)

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



    def check_collision(self,next_rect,you):
        return next_rect.colliderect(you)

    def collide(self,you):
        pass
    def move(self,dx,dy):
        next_pos = (pos[0]+dx,pos[1]+dy)
        next_rect =  pygame.Rect(self.pos[0]+dx,self.pos[1]+dy,glb.W,glb.H)
        #check collide
            #...
        if dx > 0 :
            self.direction = glb.DIRECTION_RIGHT
        if dx < 0 :
            self.direction = glb.DIRECTION_LEFT
        if dy > 0 :
            self.direction = glb.DIRECTION_DOWN
        if dy < 0 :
            self.direction = glb.DIRECTION_UP
        self.pos = next_pos
        self.rect = next_rect
    
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

    def move(self,dx,dy):
        super().move(dx,dy)


    def collide(self,you):
        if not self.check_collision(you):
            return None
        if you.etype == ETYPE_WALL:
            collide_wall(self,you)
        if you.etype == ETYPE_DOOR:
            pass

    def collide_wall(self,wall):
        pass

