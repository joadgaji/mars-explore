try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        from pygame.locals import *
        import random
        import threading
        import thread
        from Robot import *
        from Obstaculo import *
        from Nave import *


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"



screen = pygame.display.set_mode((600,600))
background = pygame.image.load('Resources/mars2.gif').convert()
screen.blit(background, (0, 0))
robots = []
obstaculos = []
mapa = {}
rand = random.randint(0,120)
mutex = threading.Lock()

nave = Nave(rand)
mapa[rand] = 'nave'

for x in range(5):
        rand = random.randint(0,120)
        while mapa.has_key(rand):
              rand = random.randint(0,120)
        obs = Obstaculo(rand)
        mapa[rand] = 'obstaculo'
        obstaculos.append(obs)
        print rand
        
for x in range(5):
        rand = random.randint(0,120)
        while mapa.has_key(rand):
              rand = random.randint(0,120)
        o = Robot(rand)
        mapa[rand] = 'robot'
        robots.append(o)
        print rand
        
for o in robots:
        thread.start_new_thread(o.move, (mapa, mutex ,))
        
while 1:
        for event in pygame.event.get():
                if event.type == QUIT:
                        for o in robots:
                                o.seguir = False
                        pygame.quit()

        screen.blit(background, (0,0))
        screen.blit(nave.image, nave.pos)
        for o in obstaculos:
                screen.blit(o.image, o.pos)
        for o in robots: 
                 screen.blit(o.image, o.pos)
        pygame.display.update()
        pygame.time.delay(50)
            

            
