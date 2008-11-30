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
        from Robot import *


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class RobotEspecial(Robot):
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
        self.capacidad = 1000
        self.cargadas = 0
        self.obstaculo = False
        self.rand = 0
        self.capas = []

        self.fontrob = fontrob
        self.surface = self.fontrob.render(str(self.cargadas), True, (10,37,150))
        self.image = pygame.image.load('Resources/RobotEspecial.png').convert_alpha()
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
                    if self.evitarobs(mapa,mutex, self.nave):
                        break
                if a == 2:
                    if self.descarga(mapa, mutex, self.nave):
                        break
                if a == 3:
                    if self.cargaesme(mapa, mutex, ""):
                        break
                if a == 4:
                    if self.explorar(mapa, mutex):
                        break

    def descarga(self, mapa, mutex, posmapnew):
            if self.cargadas != 0:
                self.cambiarnum(-1, mutex)
                mutex.acquire()
                mapa[self.nave].aumentap(mutex)
                mutex.release()
                return True
            return False
