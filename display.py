import pygame
import glb
#display hero state and monster state
pygame.font.init()
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 20)


def wait_enter():
    glb.screen.fill((0, 0, 0),pygame.Rect(0,0,600,400))

    info_displayer.info_nextline("Press Enter to continue ..... ")
    glb.render_all()

    go = False
    while not go:
        events = pygame.event.get()
        for event in events:
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    go = True



class StateTextDisplayer:
    def __init__(self,font_renderer):
      self.font_renderer = font_renderer

    def show_hero_state(self):

      glb.screen.fill((0, 0, 0),pygame.Rect(600,0,200,400) )


      text = font_renderer.render('HP %d'%( glb.hero.hp),1,(255,255,255))
      glb.screen.blit( text ,  (610,10))

      text = font_renderer.render('ROOM %d'%( glb.hero.current_room ),1,(255,255,255) )
      glb.screen.blit( text ,  (610,30))

      text = font_renderer.render('CD %d'%( glb.hero.current_cd ),1,(255,255,255) )
      glb.screen.blit( text ,  (610,50))

    def show_monsters_state(self):
      start_y = 70
      for monster in glb.monster_list:
          text = font_renderer.render('Monster HP %d'%(monster.hp),1,(255,255,255))
          glb.screen.blit( text ,  (610,start_y))

          start_y+=20
      




class InfoTextDisplayer:

    def __init__(self,font_renderer):
      self.font_renderer = font_renderer
      self.info_history = []
      self.offset_y = 410

    def cls_info(self):
      for  history in self.info_history:
         pos,text = history[0],history[1]
         print(pos)
         print(text)
         black = font_renderer.render(text,1,(0,0,0) )
         glb.screen.blit( black , pos)
         self.info_history = []
         self.offset_y = 410

    def show_info(self,text,pos=(0,410)):
      label = font_renderer.render(text,1,(255,255,255) )
      glb.screen.blit(label,pos)
      self.info_history.append((pos,text))
      self.offset_y+=20

    def  info_nextline(self,text):
      label = font_renderer.render(text,1,(255,255,255) )
      pos = (0,self.offset_y)
      glb.screen.blit(label,pos)

      self.info_history.append((pos,text))
      self.offset_y+=20


state_displayer = StateTextDisplayer(font_renderer)
info_displayer = InfoTextDisplayer(font_renderer)



