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

class Esmeralda:
        def __init__(self, mapaxy, esmeraldas, fontesme):
                self.positionx = (mapaxy%12)*50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy
                self.speed = 5
                self.esmeraldas = esmeraldas
                self.movimiento = 5
                self.frame = 10
                
                self.fontesme = fontesme
                self.surface = fontesme.render(str(self.esmeraldas), True, (200,200,50))
                self.image = pygame.image.load('Resources/esmeralda.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
                self.postext = self.surface.get_rect().move(self.positionx +25 -(self.surface.get_size()[0]/ 2), self.positiony + 25 - (self.surface.get_size()[1]/ 2))

        def quitarpiedra(self, mapa, mutex):
                mutex.acquire()
                self.esmeraldas = self.esmeraldas - 1
                if(self.esmeraldas == 0):
                        del mapa[self.mapaxy]
                mutex.release()
                self.surface = self.fontesme.render(str(self.esmeraldas), True, (200,200,50))
                self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))

        def postext(self, surface):
                size = surface.get_size()
                height = size[0]/ 2
                width = size[1]/ 2
                return (self.positionx +25 - height, self.positiony + 25 - width)

        def mytype(self):
                return "esmeralda"

