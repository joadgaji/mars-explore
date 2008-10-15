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
        def __init__(self, mapaxy, capacidad, fontrob, nave):
                self.positionx = (mapaxy%12) *50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy
                self.speed = 5
                self.movimiento = 5

                self.nave = nave
                
                self.movanterior = 0
                self.movactual = 0
                
                self.frame = 10
                self.seguir = True
                self.capacidad = capacidad
                self.cargadas = 0
                self.obstaculo = False
                self.rand = 0
                self.capas = []

                self.fontrob = fontrob
                self.surface = self.fontrob.render(str(self.cargadas), True, (10,37,150))
                self.image = pygame.image.load('Resources/robot2.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
                self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))

        def dispararcapas(self, capas, mapa, mutex, *args):
                while self.seguir:
                        for event in pygame.event.get():
                                if event.type in (QUIT, KEYDOWN):
                                        exit()
                        mutex.acquire()
                        self.capas = capas
                        mutex.release()
                        for a in self.capas:
                                if a == 1:
                                        if self.evitarobs(mapa,mutex):
                                                break
                                if a == 2:
                                        if self.regresoanave(mapa,mutex):
                                                break
                                if a == 3:
                                        if self.cargaesme(mapa, mutex):
                                                break
                                if a == 4:
                                        if self.explorar(mapa, mutex):
                                                break

                                     
        def mytype(self):
                return "robot"

        def regresoanave(self, mapa, mutex):
                movx = (self.nave.positionx / 50) - self.mapaxy%12
                movy = (self.nave.positiony / 50) - self.mapaxy/12
                entreacapa = False
                posmapnew = 0
                rand = 0
                
                if self.cargadas > 0:
                        entreacapa = True
                
                        if not self.haynave(mapa, mutex):
                                ###
                                if random.randint(0,1):
                                        if movx < 0:
                                                rand = 4
                                                self.move(mapa, mutex, 4)
                                        elif movx > 0:
                                                rand = 3
                                                self.move(mapa, mutex, 3)
                                else:
                                        if movy > 0:
                                                rand = 2
                                                self.move(mapa, mutex, 2)
                                        elif movy < 0:
                                                rand = 1
                                                self.move(mapa, mutex, 1)

                return entreacapa
                
                        
        def haynave(self, mapa, mutex):
                estanave = False
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
                                if mapa[posmapnew].mytype() == "soylanavepitoembocas":
                                        estanave = True                                        
                                        self.descarga(mapa, mutex, posmapnew)
                        mutex.release()
                return estanave


        def descarga(self, mapa, mutex, posmapnew):
                #while self.cargadas != 0:
                        self.cambiarnum(-1, mutex)
                        mapa[posmapnew].aumentap(mutex)


        def cargaesme(self, mapa, mutex):
                cargue = False
                if self.cargadas < self.capacidad:
                        h = self.hayesme(mapa,mutex)
                        while h != -1:
                                if self.cargadas < self.capacidad:
                                        cargue = True
                                        self.carga(h, mapa, mutex)
                                if not(mapa.has_key(h)) or (self.cargadas == self.capacidad):
                                        h = -1
                return cargue

                
        def carga(self, posesme, mapa, mutex):
                mutex.acquire()
                if mapa.has_key(posesme):
                        mapa[posesme].quitarpiedra(mapa, mutex)
                        self.cambiarnum(1,  mutex)
                mutex.release()

        def hayesme(self, mapa, mutex):
                pospiedra = -1
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
                                if mapa[posmapnew].mytype() == "esmeralda" and self.cargadas < self.capacidad:
                                        pospiedra = posmapnew
                        mutex.release()

                return pospiedra

        def cambiarnum(self,num, mutex):
                self.cargadas = self.cargadas + num
                self.surface = self.fontrob.render(str(self.cargadas), True, (10,37,150))
                if self.cargadas == self.capacidad:
                        self.surface = self.fontrob.render(str(self.cargadas), True, (250,30,30))
                
                self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))
                pygame.time.delay(40)


        def evitarobs(self, mapa, mutex):
                if not(self.obstaculo):
                        return False
                elif self.cargadas == 0:
                        movactual = {1 : 2, 2 : 1, 3 : 4, 4 : 3}[self.movanterior]
                        self.move(mapa, mutex, movactual)
                        #self.move(mapa, mutex, random.randint(1,4))
                        self.obstaculo = False
                else:
                        movactual = {1 : 2, 2 : 1, 3 : 4, 4 : 3}[self.movanterior]
                        self.move(mapa, mutex, movactual)
                        #self.move(mapa, mutex, movactual)
                        movx = (self.nave.positionx / 50) - self.mapaxy%12
                        movy = (self.nave.positiony / 50) - self.mapaxy/12
                        if movactual == 1 or movactual == 2:
                                if movx < 0:
                                        rand = 4
                                        self.move(mapa, mutex, 4)
                                elif movx > 0:
                                        rand = 3
                                        self.move(mapa, mutex, 3)
                                elif movx == 0:
                                        self.move(mapa, mutex, random.randint(3,4))
                        else:
                                if movy > 0:
                                        rand = 2
                                        self.move(mapa, mutex, 2)
                                elif movy < 0:
                                        rand = 1
                                        self.move(mapa, mutex, 1)
                                elif movy == 0:
                                        self.move(mapa, mutex, random.randint(1,2))
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
                                self.obstaculo = True
                else:
                        rand = 5
                        self.obstaculo = True
                mutex.release()
                self.movimiento = rand
                for i in range(self.frame):
                        self.movimientos()
                        pygame.time.delay(30)

                return rand


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
                        pygame.time.delay(30)

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
                        
        def movedown(self):
                self.pos = self.pos.move(0, self.speed)
                self.postext = self.postext.move(0, self.speed)
                        
        def moveright(self):
                self.pos = self.pos.move(self.speed, 0)
                self.postext = self.postext.move(self.speed, 0)

        def moveleft(self):
                self.pos = self.pos.move(-self.speed, 0)
                self.postext = self.postext.move(-self.speed, 0)
                
