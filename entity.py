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

    def render(self):
        for img in self.img_list:
            self.render_rect(img)

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



