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


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class Robot:
        def __init__(self, mapaxy, capacidad, fontrob):
                self.positionx = (mapaxy%12) *50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy
                self.speed = 5
                self.movimiento = 5
                
                self.movanterior = 0
                self.movactual = 0
                
                self.frame = 10
                self.seguir = True
                self.capacidad = capacidad
                self.cargadas = capacidad
                self.obstaculo = False
                self.rand = 0
                self.capas = []

                self.fontrob = fontrob
                self.surface = self.fontrob.render(str(capacidad), True, (10,37,150))
                self.image = pygame.image.load('Resources/robot2.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
                self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))

        def mytype(self):
                return "robot"
        
        def dispararcapas(self, capas, mapa, mutex, *args):
                while self.seguir:
                        for event in pygame.event.get():
                                if event.type in (QUIT, KEYDOWN):
                                        exit()
                        #self.cargaesme(mapa, mutex)
                        mutex.acquire()
                        self.capas = capas
                        mutex.release()
                        for i in self.capas:
                                if {1: self.evitarobs(mapa, mutex),
                                    3: self.cargaesme(mapa, mutex),
                                    5: self.explorar(mapa, mutex)}[i]:
                                        break

        def cargaesme(self, mapa, mutex):
                cargue = False
                h = self.hayesme(mapa,mutex)
                while h:
                        if self.cargadas:
                                cargue = True
                                self.carga(mapa[h], mapa, mutex)
                        h = self.hayesme(mapa, mutex)

                return cargue
        
        def carga(self, esme, mapa, mutex):
                esme.quitarpiedra(mapa, mutex)

        def hayesme(self, mapa, mutex):
                pospiedra = None
                for i in range(1,5):
                        if i == 1:
                                posmapnew = self.mapaxy - 12
                        if i == 2:
                                posmapnew = self.mapaxy + 12
                        if i == 3:
                                posmapnew = self.mapaxy + 1
                                if ( posmapnew % 12 ) == 0:
                                        posmapnew  = self.mapaxy
                        if i == 4:
                                posmapnew = self.mapaxy - 1
                                if ( posmapnew % 12 ) == 11:
                                        posmapnew = self.mapaxy
                        mutex.acquire()
                        if (mapa.has_key(posmapnew)):
                                if mapa[posmapnew].mytype() == "esmeralda":
                                        pospiedra = posmapnew
                                        self.subirnu(mapa, mutex)
                        mutex.release()

                return pospiedra

        def subirnu(self, mapa, mutex):
                self.cargadas = self.cargadas - 1
                self.surface = self.fontrob.render(str(self.cargadas), True, (10,37,150))
                self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))
                pygame.time.delay(40)

        
        def evitarobs(self, mapa, mutex):
                if not(self.obstaculo):
                        return False
                else:
                        movactual = {1 : 2, 2 : 1, 3 : 4, 4 : 3}[self.movanterior]
                        self.move(mapa, mutex, movactual)
                        self.move(mapa, mutex, movactual)
                        self.move(mapa, mutex, 1)
                        self.obstaculo = False

        def move(self, mapa, mutex, movactual):
                rand = movactual
                posmapnew = 0
                
                if rand == 1:
                        posmapnew = self.mapaxy - 12
                if rand == 2:
                        posmapnew = self.mapaxy + 12
                if rand == 3:
                        posmapnew = self.mapaxy + 1
                        if ( posmapnew % 12 ) == 0:
                                posmapnew  = self.mapaxy
                if rand == 4:
                        posmapnew = self.mapaxy - 1
                        if ( posmapnew % 12 ) == 11:
                                posmapnew = self.mapaxy

                self.movanterior = rand
                mutex.acquire()        
                if posmapnew >= 0  and posmapnew < 120:
                        if not(mapa.has_key(posmapnew)):
                                mapa[posmapnew] = self
                                del mapa[self.mapaxy]
                                self.mapaxy = posmapnew
                        else:
                                rand = 5
                else:
                        rand = 5
                mutex.release()
                self.movimiento = rand
                for i in range(self.frame):
                        self.movimientos()
                        pygame.time.delay(40)
        
        
        def explorar(self, mapa, mutex):
                rand = random.randint(1,4)
                posmapnew = 0
                
                if rand == 1:
                        posmapnew = self.mapaxy - 12
                if rand == 2:
                        posmapnew = self.mapaxy + 12
                if rand == 3:
                        posmapnew = self.mapaxy + 1
                        if ( posmapnew % 12 ) == 0:
                                posmapnew  = self.mapaxy
                if rand == 4:
                        posmapnew = self.mapaxy - 1
                        if ( posmapnew % 12 ) == 11:
                                posmapnew = self.mapaxy

                self.movanterior = rand
                
                mutex.acquire()
                if posmapnew >= 0  and posmapnew < 120:
                        if not(mapa.has_key(posmapnew)):
                                mapa[posmapnew] = self
                                del mapa[self.mapaxy]
                                self.mapaxy = posmapnew
                        else:
                                rand = 5
                                self.obstaculo = True
                else:
                        rand = 5
                        self.obstaculo = True
                mutex.release()
                
                self.movimiento = rand
                for i in range(self.frame):
                        self.movimientos()
                        pygame.time.delay(20)

                return True

        def movimientos(self):
                if self.movimiento == 1:
                        self.moveup()
                elif self.movimiento == 2:
                        self.movedown()
                elif self.movimiento == 3:
                        self.moveright()
                elif self.movimiento == 4:
                        self.moveleft()
                
        def postext(self, surface):
                return ((self.mapaxy%12) *50 +25 - height, (self.mapaxy/12) *50 + 25 - width)
        
                
        def moveup(self):
                self.pos = self.pos.move(0, -self.speed)
                self.postext = self.postext.move(0, -self.speed)
                #if self.pos.top < 0:
                 #       self.pos.top = 500
                        
        def movedown(self):
                self.pos = self.pos.move(0, self.speed)
                self.postext = self.postext.move(0, self.speed)
                #if self.pos.top > 500:
                 #       self.pos.top = 0
                        
        def moveright(self):
                self.pos = self.pos.move(self.speed, 0)
                self.postext = self.postext.move(self.speed, 0)
                #if self.pos.right > 600:
                 #       self.pos.left = 0

        def moveleft(self):
                self.pos = self.pos.move(-self.speed, 0)
                self.postext = self.postext.move(-self.speed, 0)
                #if self.pos.right < 0:
                 #       self.pos.left = 600
                 
##        def regresoanave(self):
                
