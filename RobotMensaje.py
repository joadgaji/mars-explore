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

class RobotMensaje(Robot):
    def __init__(self, mapaxy, capacidad, fontrob, nave, nombre):
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

        self.nombre = nombre
        
        self.dejarmoronas = False
        self.nummorona = 1
        self.valuemorona = 0
        
        self.fontrob = fontrob
        self.surface = self.fontrob.render(str(self.cargadas), True, (10,37,150))
        self.image = pygame.image.load('Resources/robot2.png').convert_alpha()
        self.pos = self.image.get_rect().move(self.positionx, self.positiony)
        self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))

    def dispararcapas(self, capas, mapa, mutex, mensajes, *args):
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
                                    if self.cargaesme(mapa, mutex, mensajes):
                                            break
                            if a == 4:
                                    if self.leermensaje(mapa, mutex, mensajes):
                                            break
                            if a == 5:
                                    if self.explorar(mapa, mutex):
                                            break

    def cargaesme(self, mapa, mutex, mensajes):
        cargue = False
        if self.cargadas < self.capacidad:
                h = self.hayesme(mapa,mutex)
                while h != -1:
                        if self.cargadas < self.capacidad:
                                cargue = True
                                self.carga(h, mapa, mutex)
                        if mapa.has_key(h) and self.cargadas == self.capacidad:
                            if h not in mensajes:
                                self.mandaMensaje(mensajes, h, mutex)
                        if not(mapa.has_key(h)):
                            mutex.acquire()
                            if h in mensajes:
                                del mensajes[mensajes.index(h)]
                            mutex.release()
                        if not(mapa.has_key(h)) or self.cargadas == self.capacidad:
                                h = -1

        return cargue   

    def mandaMensaje(self, mensajes, posesme, mutex):
        mutex.acquire()
        mensajes.append(posesme)
        mutex.release()
        print "(Informar-KQML"
        print ":sender", self.nombre
        print ":receiver broadcast"
        print ":language KQML"
        print ":ontology marte-sinamigos"
        print ":content hay esmeraldas en:", posesme, ")"

    def leermensaje(self, mapa, mutex, mensajes):
        entrecapa = False
        posesmeralda = -1
        mutex.acquire()
        
        for x in mensajes:
            entrecapa = self.factorDistancia(mapa, mutex, x)
            if entrecapa:
                posesmeralda = x
                break
        mutex.release()
            
        if entrecapa:
            self.irAEsme(mapa, mutex, posesmeralda)
            
    def factorDistancia(self, mapa, mutex, posesme):
        #print mapa, "mapa - ", posesme, "PosEsme"
        movx = 0
        movy = 0
        if mapa.has_key(posesme):
            movx = (mapa[posesme].positionx / 50) - self.mapaxy%12
            movy = (mapa[posesme].positiony / 50) - self.mapaxy/12
        else:
            return False
        posmapnew = 0
        rand = 0
        
        if movx < 6 and movx > -6 and movy < 6 and movy > -6:
            return True

        return False

    def irAEsme(self, mapa, mutex, posesmeralda):
        print "Yo si le voy le voy al toluca"
        movx = (mapa[posesmeralda].positionx / 50) - self.mapaxy%12
        movy = (mapa[posesmeralda].positiony / 50) - self.mapaxy/12
        posmapnew = 0
        rand = 0
        
        if not self.hayEsme(mapa, mutex, posesmeralda):
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

        return 

    def hayEsme(self, mapa, mutex, posesmeralda):
        estaesmeralda = False
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
                                
                if posesmeralda == posmapnew:
                    estaesmeralda = True
                    
        return estaesmeralda
