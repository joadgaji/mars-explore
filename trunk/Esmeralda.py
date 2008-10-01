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
        def __init__(self, mapaxy, esmeraldas, surface):
                self.positionx = (mapaxy%12)*50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy
                self.speed = 5
                self.esmeraldas = esmeraldas
                self.movimiento = 5
                self.frame = 10
                self.surface = surface
                self.image = pygame.image.load('Resources/esmeralda.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
                self.postext = self.surface.get_rect().move(self.positionx +25 -(surface.get_size()[0]/ 2), self.positiony + 25 - (surface.get_size()[1]/ 2))

        def quitarpiedra(self):
                self.esmeraldas = self.esmeraldas - 1

        def postext(self, surface):
                size = surface.get_size()
                height = size[0]/ 2
                width = size[1]/ 2
                return (self.positionx +25 - height, self.positiony + 25 - width)

        def mytype(self):
                return "esmeralda"

