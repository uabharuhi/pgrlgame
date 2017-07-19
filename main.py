import glb
import entity
import pygame

glb.init_game()
glb.render_all()

hero = glb.hero
#main loop
running = True
while running:
    glb.clock.tick(10)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            hero.move(-1*glb.W, 0)
        if key[pygame.K_RIGHT]:
            hero.move(glb.W, 0)
        if key[pygame.K_UP]:
            hero.move(0, -1*glb.H)
        if key[pygame.K_DOWN]:
            hero.move(0,glb.H)
    glb.render_all()
  
    #print(key)