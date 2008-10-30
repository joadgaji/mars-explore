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
        from Robot import Robot


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class RobotMoronas(Robot):
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

        self.dejarmoronas = False
        self.nummorona = 1
        self.valuemorona = 0
        
        self.fontrob = fontrob
        self.surface = self.fontrob.render(str(self.cargadas), True, (10,37,150))
        self.image = pygame.image.load('Resources/robot2.png').convert_alpha()
        self.pos = self.image.get_rect().move(self.positionx, self.positiony)
        self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))


    def dispararcapas(self, capas, mapa, mutex, moronas, *args):
                while self.seguir:
                        for event in pygame.event.get():
                                if event.type in (QUIT, KEYDOWN):
                                        exit()
                        mutex.acquire()
                        self.capas = capas
                        mutex.release()
                        for a in self.capas:
                                if a == 1:
                                        if self.evitarobs(mapa,mutex, moronas):
                                                break
                                if a == 2:
                                        if self.regresoanave(mapa,mutex, self.nave, moronas):
                                                break
                                if a == 3:
                                        if self.cargaesme(mapa, mutex, "moronas"):
                                                break
                                if a == 4:
                                        if self.siguemoronas(mapa, mutex, moronas):
                                                break
                                if a == 5:
                                        if self.explorar(mapa, mutex):
                                                break


    def dejamorona(self, moronas):
            moronas[self.mapaxy] = self.nummorona
            self.nummorona = self.nummorona + 1


    def regresoanave(self, mapa, mutex, cosa, moronas):
        movx = (cosa.positionx / 50) - self.mapaxy%12
        movy = (cosa.positiony / 50) - self.mapaxy/12
        entreacapa = False
        posmapnew = 0
        rand = 0
        
        if self.cargadas > 0 :
                if self.dejarmoronas and self.hayAlgo(mapa, mutex, cosa, "moronas") == -1:
                        mutex.acquire()
                        self.dejamorona(moronas)
                        mutex.release()
                entreacapa = True

                if self.hayAlgo(mapa, mutex,cosa, "moronas") == -1:
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


    def siguemoronas(self, mapa, mutex, moronas):
        seguimoro = False
        self.valuemorona = 10000
        m_actual = self.haymorona(mutex, moronas, mapa)
        while m_actual != -1:
            seguimoro = True
            
            contador = 10
            while self.move(mapa, mutex, self.movactual) == 5 and contador:
                    self.obstaculo = False
                    contador = contador - 1
            mutex.acquire()
            if moronas.has_key(self.mapaxy):
                    self.valuemorona = moronas[self.mapaxy]
                    del moronas[self.mapaxy]
                    if self.valuemorona == 1:
                            mutex.release()
                            return seguimoro
            mutex.release()
            m_actual = self.haymorona(mutex, moronas, mapa)
        
        return seguimoro


    def haymorona(self, mutex, moronas, mapa):
        moronamenor = 10000
        indexm = -1
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
                if (moronas.has_key(posmapnew)) and moronas[posmapnew] < moronamenor:
                        moronamenor = moronas[posmapnew]
                        self.movactual = i
                        if moronamenor == self.valuemorona -1:
                                mutex.release()
                                return moronamenor

                mutex.release()
                if moronamenor > self.valuemorona and i == 4:
                        return -1
        if moronamenor == 10000:
            moronamenor = -1
        return moronamenor


    def evitarobs(self, mapa, mutex, moronas):
        if not(self.obstaculo):
                return False
        elif self.cargadas == 0:
                movactual = {1 : 2, 2 : 1, 3 : 4, 4 : 3}[self.movanterior]
                self.move(mapa, mutex, movactual)
                self.obstaculo = False
        else:
                movactual = {1 : 2, 2 : 1, 3 : 4, 4 : 3}[self.movanterior]
                self.move(mapa, mutex, movactual)
                if self.dejarmoronas:
                        mutex.acquire()
                        self.dejamorona(moronas)
                        mutex.release()
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
