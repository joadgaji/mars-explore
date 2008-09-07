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


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"



screen = pygame.display.set_mode((600,600))
background = pygame.image.load('Resources/mars2.gif').convert()
screen.blit(background, (0, 0))
robots = []
mapa = {}
rand = random.randint(0,120)
mutex = threading.Lock()

for x in range(5):
        rand = random.randint(0,120)
        o = Robot(rand)
        mapa[rand] = 'robot'
        robots.append(o)
        print rand
        
for o in robots:
        thread.start_new_thread(o.move, (mapa, mutex ,))
        
while 1:
        for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                        exit()

        screen.blit(background, (0,0))
        for o in robots: 
                 screen.blit(o.image, o.pos)
        pygame.display.update()
        pygame.time.delay(50)
            

            
