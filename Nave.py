try:
        import sys
        import random
        import math
        import os
        import getopt
        import pygame
        from pygame.locals import *


except ImportError, err:
        print "couldn't load module. %s" % (err)
        sys.exit(2)
        print "Import OK"

class Nave:
        def __init__(self, mapaxy, fontnave):
                self.positionx = (mapaxy%12) *50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy

                self.piedras = 0
                
                self.fontnave = fontnave
                self.surface = fontnave.render(str(self.piedras), True, (240,20,20))
                
                self.image = pygame.image.load('Resources/nave.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
                self.postext = self.surface.get_rect().move(self.positionx +25 -(self.surface.get_size()[0]/ 2), self.positiony + 25 - (self.surface.get_size()[1]/ 2))
                
        def aumentap(self, mutex):
##                mutex.aquire()
                self.piedras = self.piedras + 1
                self.surface = self.fontnave.render(str(self.piedras), True, (240,20,20))
                self.postext = self.surface.get_rect().move(((self.mapaxy%12) *50) +25 - (self.surface.get_size()[0]/ 2), ((self.mapaxy/12) *50) + 25 - (self.surface.get_size()[1]/ 2))
##                mutex.release()

        def postext(self, surface):
                size = surface.get_size()
                height = size[0]/ 2
                width = size[1]/ 2
                return (self.positionx +25 - height, self.positiony + 25 - width)


        def mytype(self):
                return "soylanavepitoembocas"

        def get_position(self):
            return self.mapaxy
