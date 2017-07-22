import pygame
import glb
#display hero state and monster state
pygame.font.init()
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 20)

class StateTextDisplayer:
    def __init__(self,font_renderer):
      self.font_renderer = font_renderer

    def show_hero_state(self):

      glb.screen.fill((0, 0, 0),pygame.Rect(600,0,200,400) )


      text = font_renderer.render('HP %d'%( glb.hero.hp),1,(255,255,255))
      glb.screen.blit( text ,  (610,10))

      text = font_renderer.render('ROOM %d'%( glb.hero.current_room ),1,(255,255,255) )
      glb.screen.blit( text ,  (610,30))




class InfoTextDisplayer:

    def __init__(self,font_renderer):
      self.font_renderer = font_renderer
      self.info_history = []
      self.offset_y = 410

    def cls_info(self):
      for  pos,text in self.info_history:
         black = font_renderer.render(text,1,(0,0,0) )
         glb.screen.blit( black , pos)
         self.info_history = []
         self.offset_y = 410

    def show_info(self,text,pos=(0,410)):
      text = font_renderer.render(text,1,(255,255,255) )
      glb.screen.blit(text,pos)
      self.info_history.append((pos,text))
      self.offset_y+=20

    def  info_nextline(self,text):
      text = font_renderer.render(text,1,(255,255,255) )
      pos = (0,self.offset_y)
      glb.screen.blit(text,pos)

      self.info_history.append((pos,text))
      self.offset_y+=20


state_displayer = StateTextDisplayer(font_renderer)
info_displayer = InfoTextDisplayer(font_renderer)


