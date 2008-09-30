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
        def __init__(self, posx, posy):
                self.posx = posx *50
                self.posy = posy *50
                self.mapaxy = posx * posy
                self.image = pygame.image.load('Resources/nave.png').convert_alpha()
                self.pos = self.image.get_rect().move(self.posx, self.posy)
                self.piedras = 0
                
        def add_piedras(self, num):
            self.piedras = self.piedras + num

        def get_position(self):
            return self.mapaxy

        def mytype(self):
                return "nave"
