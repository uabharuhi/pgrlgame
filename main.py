import glb
#import entity
import pygame


def gg():
    pygame.quit()

glb.init_game()
glb.render_all()

screen = glb.screen
#main loop
move_contraint = False #only can move once in one tick
key_lock = [False,False,False,False]

while glb.running:
    glb.clock.tick(4)
    move_contraint = False
    glb.hero.decrease_cd()
    #pressed = False
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            glb.running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            glb.running = False
        #can only allow move on axis
        if e.type == pygame.KEYDOWN: #and not  press_flag: # for only once
            if True not in key_lock :
                if e.key == pygame.K_UP and not key_lock[0]:
                    if not move_contraint:
                            glb.hero.move(0, -1*glb.hero.speed)
                            move_contraint = True
                    key_lock[0] = True
                if e.key == pygame.K_RIGHT and not key_lock[1]:
                    if not move_contraint:
                            glb.hero.move(glb.hero.speed,0)
                            move_contraint = True
                    key_lock[1] = True
                if e.key == pygame.K_DOWN and not key_lock[2]:
                    if not move_contraint:
                            glb.hero.move(0,glb.hero.speed)
                            move_contraint = True
                    key_lock[2] = True
                if e.key == pygame.K_LEFT and not key_lock[3]:
                    if not move_contraint:
                            glb.hero.move(-1*glb.hero.speed, 0)
                            move_contraint = True
                    key_lock[3] = True
            #attack can using when press other button
            if e.key == pygame.K_a :
                glb.hero.attack()
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_UP and key_lock[0]:
                key_lock[0] = False
            if e.key == pygame.K_RIGHT and  key_lock[1]:
                key_lock[1] = False
            if e.key == pygame.K_DOWN and key_lock[2]:
                key_lock[2] = False
            if e.key == pygame.K_LEFT and key_lock[3]:
                key_lock[3] = False

    for move_obj in glb.movable_list[:] :
        if move_obj == glb.hero:
            continue
        dx,dy = move_obj.next_step()
        move_obj.move(dx,dy)
        #move_obj.move(dx,dy)
    screen.fill((0, 0, 0),pygame.Rect(0,0,500,500))
    glb.render_all()


gg()

    #dl = [ door  for door in glb.door_list if door.room_id == 0 ]
   # print(len(dl))
    #print(key)
