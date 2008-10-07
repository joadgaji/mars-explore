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
        from Robot import Robot
        from Obstaculo import *
        from Nave import *
        from Esmeralda import *
       ## from GeneradorDeObs import *


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"


pygame.init()
screen = pygame.display.set_mode((600,600))
background = pygame.image.load('Resources/mars2.gif').convert()
cond = threading.Condition()
screen.blit(background, (0, 0))
robots = []
obstaculos = []
esmeraldas = []
mapa = {}
rand = random.randint(0,120)
mutex = threading.Lock()
capas = [1,3,5]
nave = Nave(rand)
mapa[rand] = nave

def generarObs(x):
    opciones =[(0,0), (11,13), (11,12)]
    obs = []
    
    while (x > 0):
        if x < 3:
            figuras = 0
        else:
            figuras  = random.randint(0,2)
            
        if figuras == 0:
            obs = obs + generarRand()
            x = x - 1
        else:
            obs = obs + generarRandParaTres(opciones[figuras][0], opciones[figuras][1])        
            x = x - 3 
    return obs
        
def generarRand():
        rand = random.randint(0,120)
        while mapa.has_key(rand):
              rand = random.randint(0,120)
        return [rand]

def generarRandParaTres(uno, dos):
        rand1 = random.randint(0,120)
        rand2 = rand1 + uno
        rand3 = rand2 + dos
        if (mapa.has_key(rand2) or mapa.has_key(rand3) or mapa.has_key(rand1)):
            generarRandParaTres(uno, dos)
        return [rand1, rand2, rand3]
        

listaPos = generarObs(10)

for i in listaPos:
        obs = Obstaculo(i)
        mapa[i] =  obs
        obstaculos.append(obs)

        
for x in range(5):
        
        rand = random.randint(0,120)
        while mapa.has_key(rand):
                rand = random.randint(0,120)
                
        randcap = random.randint(5,25)
        fontrob = pygame.font.SysFont("arial", 15, True);
        o = Robot(rand, randcap, fontrob)
        mapa[rand] = o
        robots.append(o)
        print randcap

for x in range(10):
        
        rand = random.randint(0,120)
        while mapa.has_key(rand):
                rand = random.randint(0,120)
                
        randp = random.randint(50,200)
        fontesme = pygame.font.SysFont("arial", 15, True);
        esme = Esmeralda(rand, randp, fontesme)
        mapa[rand] = esme
        esmeraldas.append(esme)

for o in robots:
        thread.start_new_thread(o.dispararcapas, (capas, mapa, mutex,))
        
while 1:
        for event in pygame.event.get():
                if event.type == QUIT:
                        for o in robots:
                                o.seguir = False
                        pygame.quit()
                        exit()

        screen.blit(background, (0,0))
        screen.blit(nave.image, nave.pos)
        for o in obstaculos:
                screen.blit(o.image, o.pos)
        for o in robots: 
                 screen.blit(o.image, o.pos)
                 screen.blit(o.surface, o.postext)
        for o in esmeraldas:
                if o.esmeraldas != 0:
                        screen.blit(o.image, o.pos)
                        screen.blit(o.surface, o.postext)
        #cond.notifyAll()
        pygame.display.update()
        pygame.time.delay(30)
