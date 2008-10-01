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
        def __init__(self, mapaxy):
                self.positionx = (mapaxy%12) *50
                self.positiony = (mapaxy/12) *50
                self.mapaxy = mapaxy
                self.image = pygame.image.load('Resources/nave.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.positionx, self.positiony)
                self.piedras = 0
                
        def add_piedras(self, num):
            self.piedras = self.piedras + num

        def get_position(self):
            return self.mapaxy
