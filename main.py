import glb
import entity
import pygame

glb.init_game()

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
    #print(key)