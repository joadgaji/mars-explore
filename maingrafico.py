try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        from pygame.locals import *
        ##import random
        import threading
        import thread
        from Robot import Robot
        from Obstaculo import *
        from Nave import *
        from Esmeralda import *
        from RobotMoronas import *
        from RobotMensaje import *


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"


class maingrafico():

        def __init__(self, agentes, esme, orden, obs,tipoCom):
            self.agentes = agentes
            self.esme = esme
            self.orden = orden
            self.obs = obs
            
            self.tipoCom = tipoCom
            if tipoCom == 'Moronas':
                    self.moronas = True
            else:
                       self.moronas = False



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
            capas = orden
            fontnave = pygame.font.SysFont("arial", 15, True);
            posnave = rand
            nave = Nave(posnave, fontnave)
            mapa[posnave] = nave

            moronas = {}
            mensajes = []
            listaPos = self.generarObs(obs,mapa)

            for i in listaPos:
                    obs = Obstaculo(i)
                    mapa[i] =  obs
                    obstaculos.append(obs)

                    
            for x in range(self.agentes):
                    
                    rand = random.randint(0,120)
                    while mapa.has_key(rand):
                            rand = random.randint(0,120)
       
                    randcap = random.randint(5,10)
                    fontrob = pygame.font.SysFont("arial", 15, True);
                   
                    if self.tipoCom == 'Moronas':
                            o = RobotMoronas(rand, randcap, fontrob, nave)
                            
                    elif self.tipoCom == 'Reactivos':
                            
                            o = Robot(rand, randcap, fontrob, nave)
                    elif self.tipoCom == 'KQML':
                            o = RobotMensaje(rand, randcap, fontrob, nave, "robot"+str(x))
                
                    mapa[rand] = o
                    robots.append(o)
                    

            listaEsme = []
            a = self.esme
            while a > 30:
                xrand = random.randint(3,30)
                listaEsme = listaEsme + [xrand]
                a = a - xrand     
            if a <= 30:
                    listaEsme = listaEsme + [a]
                    
            for x in listaEsme:
                    
                    rand = random.randint(1,120)
                    while mapa.has_key(rand):
                            rand = random.randint(1,120)
                            
                    randp = x
                    fontesme = pygame.font.SysFont("arial", 15, True);
                    esme = Esmeralda(rand, randp, fontesme)
                    mapa[rand] = esme
                    esmeraldas.append(esme)

            for o in robots:
                    
                    if self.tipoCom == 'Moronas':
                            thread.start_new_thread(o.dispararcapas, (capas, mapa, mutex, moronas,))
                    elif self.tipoCom == 'Reactivos':
                            thread.start_new_thread(o.dispararcapas, (capas, mapa, mutex,))
                    elif self.tipoCom == 'KQML':
                            thread.start_new_thread(o.dispararcapas, (capas, mapa, mutex, mensajes,))

            while 1:
                    if nave.piedras == self.esme:
                            for o in robots:
                                    o.seguir = False
                            pygame.quit()
                            exit()
                                    
                    for event in pygame.event.get():
                            if event.type == QUIT:
                                    for o in robots:
                                            o.seguir = False
                                    pygame.quit()
                                    exit()

                    screen.blit(background, (0,0))
                    screen.blit(nave.image, nave.pos)
                    screen.blit(nave.surface, nave.postext)

                    if self.tipoCom == 'Moronas':
                            
                            mutex.acquire()
                            for o in moronas.keys():
                                            posmap = o
                                            imagemoro = pygame.image.load('Resources/morona.PNG').convert_alpha()
                                            posmoro = imagemoro.get_rect().move((posmap%12) *50,(posmap/12) *50)
                                            #surfacemoro = fontnave.render(str(moronas[o]), True, (10,37,150))

                                            screen.blit(imagemoro, posmoro)
                                            #screen.blit(surfacemoro, posmoro)
                            mutex.release()

                    for o in obstaculos:
                            screen.blit(o.image, o.pos)
                    for o in robots: 
                             screen.blit(o.image, o.pos)
                             screen.blit(o.surface, o.postext)
                    for o in esmeraldas:
                            if o.esmeraldas != 0:
                                    screen.blit(o.image, o.pos)
                                    screen.blit(o.surface, o.postext)
                    pygame.display.update()
            pygame.time.delay(20)
            
        def generarObs(self,x,mapa):
                        opciones =[(0,0), (11,13), (11,12)]
                        obs = []
                        
                        while (x > 0):
                            if x < 3:
                                figuras = 0
                            else:
                                figuras  = random.randint(0,2)
                                
                            if figuras == 0:
                                obs = obs + self.generarRand(mapa)
                                x = x - 1
                            else:
                                obs = obs + self.generarRandParaTres(opciones[figuras][0], opciones[figuras][1],mapa)        
                                x = x - 3 
                        return obs
                    
        def generarRand(self,mapa):
                    rand = random.randint(1,120)
                    while mapa.has_key(rand):
                          rand = random.randint(1,120)
                    return [rand]

        def generarRandParaTres(self,uno, dos,mapa):
                    rand1 = random.randint(1,120)
                    rand2 = rand1 + uno
                    rand3 = rand2 + dos
                    if (mapa.has_key(rand2) or mapa.has_key(rand3) or mapa.has_key(rand1)):
                        self.generarRandParaTres(uno, dos,mapa)
                    return [rand1, rand2, rand3]
                
