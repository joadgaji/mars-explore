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
                                    if self.evitarobs(mapa,mutex, self.nave):
                                            break
                            if a == 2:
                                    if self.regresoAPos(mapa,mutex,self.nave):
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
                h = self.hayAlgo(mapa,mutex, "esmeralda", "buscar")
                while h != -1:
                        if self.cargadas < self.capacidad:
                                cargue = True
                                self.carga(h, mapa, mutex)
                        mutex.acquire()
                        if mapa.has_key(h) and self.cargadas == self.capacidad:
                            if h not in mensajes:
                                self.mandaMensaje(mensajes, h, mutex)
                        if not(mapa.has_key(h)):
                            if h in mensajes:
                                del mensajes[mensajes.index(h)]
                        if not(mapa.has_key(h)) or self.cargadas == self.capacidad:
                                h = -1
                        mutex.release()

        return cargue   

    def mandaMensaje(self, mensajes, posesme, mutex):
        mensajes.append(posesme)
        print "(Informar-KQML"
        print ":sender", self.nombre
        print ":receiver broadcast"
        print ":language KQML"
        print ":ontology marte-sinamigos"
        print ":content hay esmeraldas en:", posesme, ")"
        print ""

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
                print "voy a ir",  posesmeralda
                self.irAEsme(mapa, mutex, posesmeralda)
                return True
        return False
            
    def factorDistancia(self, mapa, mutex, posesme):
        print posesme, "PosEsme"
        movx = 0
        movy = 0

        if mapa.has_key(posesme):
            movx = (posesme%12) - self.mapaxy%12
            movy = (posesme/12) - self.mapaxy/12
            if movx < 6 and movx > -6 and movy < 6 and movy > -6:
                    return True
        return False

    def irAEsme(self, mapa, mutex, posesmeralda):
        rand = 0
        while self.hayAlgo(mapa, mutex, posesmeralda, "llegarEsme") == -1:
                movx = (posesmeralda%12) - self.mapaxy%12
                movy = (posesmeralda/12) - self.mapaxy/12
                if self.obstaculo:
                        movactual = {1 : 2, 2 : 1, 3 : 4, 4 : 3}[self.movanterior]
                        self.move(mapa, mutex, movactual)
                        movx = (posesmeralda%12) - self.mapaxy%12
                        movy = (posesmeralda/12) - self.mapaxy/12
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
