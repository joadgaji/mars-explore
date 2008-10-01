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
        from Esmeralda import *


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"


pygame.init()
screen = pygame.display.set_mode((600,600))
background = pygame.image.load('Resources/mars2.gif').convert()
font2 = pygame.font.SysFont("arial", 15, True);
cond = threading.Condition()
screen.blit(background, (0, 0))
robots = []
obstaculos = []
esmeraldas = []
mapa = {}
rand = random.randint(0,120)
mutex = threading.Lock()

nave = Nave(rand)
mapa[rand] = nave

for x in range(5):
        rand = random.randint(0,120)
        while mapa.has_key(rand):
              rand = random.randint(0,120)
        obs = Obstaculo(rand)
        mapa[rand] =  obs
        obstaculos.append(obs)
        print rand
        
for x in range(5):
        rand = random.randint(0,120)
        while mapa.has_key(rand):
              rand = random.randint(0,120)
        randcap = random.randint(5,25)
        text = font2.render(str(randcap), True, (200,200,50))
        o = Robot(rand, randcap, text)
        mapa[rand] = o
        robots.append(o)
        print rand

for x in range(5):
        rand = random.randint(0,120)
        while mapa.has_key(rand):
              rand = random.randint(0,120)
        randp = random.randint(50,200)
        text = font2.render(str(randp), True, (200,200,50))
        esme = Esmeralda(rand, randp, text)
        mapa[rand] = esme
        esmeraldas.append(esme)

for o in robots:
        thread.start_new_thread(o.move, (mapa, mutex , cond,))
        
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
                 screen.blit(o.surface, o.postext)
        for o in esmeraldas:
                screen.blit(o.image, o.pos)
                screen.blit(o.surface, o.postext)
        #cond.notifyAll()
        pygame.display.update()
        pygame.time.delay(30)
