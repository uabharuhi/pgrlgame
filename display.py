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
      text = font_renderer.render('HP %d'%( glb.hero.hp),1,(255,255,255))
      glb.screen.blit( text ,  (610,10))

      text = font_renderer.render('ROOM %d'%( glb.hero.current_room ),1,(255,255,255) )
      glb.screen.blit( text ,  (610,30))




#class InfoTextDisplayer:
#    def __init__(self,):




state_displayer = StateTextDisplayer(font_renderer)
