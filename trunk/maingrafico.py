try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        from pygame.locals import *
        import random
        import thread
        from Robot import *


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"



screen = pygame.display.set_mode((600,600))
background = pygame.image.load('Resources/mars2.gif').convert()
screen.blit(background, (0, 0))
objects = []
movimientos = []
mapa = {}
rand = random.randint(0,120)
for x in range(5):
        rand = random.randint(0,120)
        o = Robot(rand)
        mapa[rand] = 'robot'
        objects.append(o)
        print rand

while 1:
        for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                        exit()
        movimientos = []
        y = 0
        for o in objects:
                
                rand = random.randint(1,4)
                posmapnew = 0
                if rand == 1:
                        posmapnew = o.mapaxy - 12
                if rand == 2:
                        posmapnew = o.mapaxy + 12
                if rand == 3:
                        posmapnew = o.mapaxy + 1
                        if ( posmapnew % 12 ) == 0:
                                posmapnew  = o.mapaxy
                if rand == 4:
                        posmapnew = o.mapaxy - 1
                        if ( posmapnew % 12 ) == 11:
                                posmapnew = o.mapaxy
                        
                if posmapnew >= 0  and posmapnew < 120:
                        if not(mapa.has_key(posmapnew)):
                                mapa[posmapnew] = 'robot'
                                del mapa[o.mapaxy]
                                o.mapaxy = posmapnew
                        else:
                                rand = 5
                else:
                        rand = 5
                        
                movimientos.append(rand)
                print y, posmapnew, o.mapaxy, rand
                y += 1
                

        for i in range(10):
                curr = 0
                screen.blit(background, (0,0))
                for o in objects:
                        o.move(movimientos[curr])
                        curr += 1
                        screen.blit(o.image, o.pos)
                pygame.time.delay(10)
                pygame.display.update()
        pygame.time.delay(20)
            
exit()
            
